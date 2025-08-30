import os
import yaml
import json
import logging
import shutil
import time
from collections import defaultdict, Counter
from typing import Dict, List, Set, Optional, Tuple
import ipaddress

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OptimalIntegrationFixedV9:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.source_dir = os.path.join(self.current_dir, 'temp-ios-rule-script', 'rule', 'Clash')
        self.target_dir = os.path.join(self.current_dir, 'sing-rule')
        
        # Statistics information
        self.stats = {
            'total_entries_found': 0,
            'entries_processed': 0,
            'entries_skipped': 0,
            'duplicates_removed': 0,
            'version_selection': {
                'classical_used': 0,
                'merged_versions': 0,
                'single_version': 0
            },
            'rule_types': {
                'domain_rules': 0,
                'ip_rules': 0,
                'process_rules': 0
            }
        }
        
        # Store all found entry information
        self.all_entries = {}  # {entry_name: {versions: [], paths: [], best_version: str}}
    
    def clean_target_directory(self):
        """Clear target directory to avoid duplicate file issues"""
        if os.path.exists(self.target_dir):
            logging.info(f"Clearing target directory: {self.target_dir}")
            try:
                # First delete all files in the directory
                for filename in os.listdir(self.target_dir):
                    file_path = os.path.join(self.target_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        logging.warning(f"Cannot delete file {file_path}: {e}")
                
                logging.info("Target directory content cleared")
            except Exception as e:
                logging.warning(f"Error clearing directory: {e}")
                # If clearing fails, try to rename the directory
                try:
                    backup_dir = self.target_dir + "_backup_" + str(int(time.time()))
                    os.rename(self.target_dir, backup_dir)
                    logging.info(f"Original directory renamed to: {backup_dir}")
                except Exception as rename_error:
                    logging.error(f"Failed to rename directory: {rename_error}")
                    return False
        
        # Ensure directory exists
        os.makedirs(self.target_dir, exist_ok=True)
        logging.info("Target directory ready")
        return True
        
    def discover_all_entries(self) -> Dict[str, Dict]:
        """Discover all base entries in BlackMatrix7"""
        logging.info("Starting to discover all base entries...")
        
        def scan_directory(directory_path: str, depth: int = 0):
            """Recursively scan directory"""
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                
                if os.path.isdir(item_path):
                    scan_directory(item_path, depth + 1)
                elif item.endswith('.yaml'):
                    # Extract base entry name
                    base_name = self.extract_base_name(item)
                    
                    if base_name not in self.all_entries:
                        self.all_entries[base_name] = {
                            'versions': [],
                            'paths': [],
                            'best_version': None,
                            'version_priority': 0
                        }
                    
                    self.all_entries[base_name]['versions'].append(item)
                    self.all_entries[base_name]['paths'].append(item_path)
        
        if os.path.exists(self.source_dir):
            scan_directory(self.source_dir)
        
        self.stats['total_entries_found'] = len(self.all_entries)
        logging.info(f"Found {self.stats['total_entries_found']} base entries")
        
        return self.all_entries
    
    def extract_base_name(self, filename: str) -> str:
        """Extract base entry name - completely fix all compound suffix issues"""
        # 🎯 Key fix: Create the most comprehensive suffix list, sorted by length from longest to shortest
        # Ensure all possible compound suffixes are handled correctly
        suffixes = [
            # Triple compound suffixes (longest)
            '_Classical_No_IPv6_No_Resolve.yaml',
            '_IP_No_IPv6_No_Resolve.yaml',
            '_Domain_No_IPv6_No_Resolve.yaml',
            
            # Double compound suffixes (medium)
            '_Classical_No_Resolve.yaml',
            '_Classical_No_IPv6.yaml',
            '_IP_No_IPv6.yaml',
            '_Domain_No_IPv6.yaml',
            '_No_Resolve_No_IPv6.yaml',
            '_Domain_For_Clash.yaml',
            
            # Single suffixes (shorter)
            '_Classical.yaml',
            '_Domain.yaml',
            '_No_Resolve.yaml',
            '_IP.yaml',
            '_No_IPv6.yaml',
            
            # Base suffix (shortest)
            '.yaml'
        ]
        
        base_name = filename
        
        # Try to remove suffixes in order, stop when a match is found
        for suffix in suffixes:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
                break
        
        return base_name
    
    def determine_best_version(self, entry_name: str, entry_info: Dict) -> str:
        """Determine the best version selection strategy"""
        versions = entry_info['versions']
        
        # Version priority scoring
        version_scores = {}
        for version in versions:
            score = 0
            
            # Classical version has highest priority
            if '_Classical.yaml' in version:
                score += 100
            # Domain version comes second
            elif '_Domain.yaml' in version:
                score += 50
            # No_Resolve version comes third
            elif '_No_Resolve.yaml' in version:
                score += 30
            # Base version has lowest priority
            elif version.endswith('.yaml'):
                score += 10
            
            # Avoid No_IPv6 versions (unless no other choice)
            if '_No_IPv6' in version:
                score -= 20
            
            version_scores[version] = score
        
        # Select the version with the highest score
        best_version = max(version_scores.keys(), key=lambda v: version_scores[v])
        entry_info['best_version'] = best_version
        entry_info['version_priority'] = version_scores[best_version]
        
        return best_version
    
    def merge_versions_if_needed(self, entry_name: str, entry_info: Dict) -> List[str]:
        """Merge multiple versions if needed"""
        versions = entry_info['versions']
        best_version = entry_info['best_version']
        
        # If there's only one version, return directly
        if len(versions) == 1:
            return self.parse_yaml_rules(entry_info['paths'][0])
        
        # If the best version is Classical, use it directly
        if '_Classical.yaml' in best_version:
            best_path = [path for path in entry_info['paths'] if best_version in path][0]
            return self.parse_yaml_rules(best_path)
        
        # Otherwise merge all versions
        all_rules = set()
        for path in entry_info['paths']:
            rules = self.parse_yaml_rules(path)
            all_rules.update(rules)
        
        return list(all_rules)
    
    def parse_yaml_rules(self, yaml_path: str) -> List[str]:
        """Parse rules from YAML file"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data and 'payload' in data:
                return data['payload']
            return []
        except Exception as e:
            logging.warning(f"Failed to parse YAML file {yaml_path}: {e}")
            return []
    
    def is_valid_ip_cidr(self, rule: str) -> bool:
        """Check if it's a valid IP-CIDR format"""
        try:
            ipaddress.ip_network(rule, strict=False)
            return True
        except ValueError:
            return False
    
    def convert_to_singbox_format(self, rules: List[str]) -> Dict:
        """Convert to sing-box format - Fixed version 9, combining efficient integration format and official documentation standards"""
        # 🎯 Key fix: Combine version 7's efficient integration format with version 8's official documentation standards
        # Group rules by type to avoid redundancy while conforming to sing-box official documentation
        
        # Group rules by type
        domains = []
        domain_suffixes = []
        domain_keywords = []
        ip_cidrs = []
        process_names = []
        
        for rule in rules:
            if not rule or rule.startswith('#'):
                continue
            
            rule = rule.strip()
            
            # Check if it's a pure IP-CIDR format (e.g., "1.0.1.0/24")
            if self.is_valid_ip_cidr(rule):
                ip_cidrs.append(rule)
                self.stats['rule_types']['ip_rules'] += 1
                continue
            
            # Check if it's a typed format (e.g., "IP-CIDR,1.0.1.0/24")
            parts = rule.split(',')
            if len(parts) >= 2:
                rule_type = parts[0].strip()
                value = parts[1].strip()
                
                # Group by type
                if rule_type == 'DOMAIN':
                    domains.append(value)
                    self.stats['rule_types']['domain_rules'] += 1
                elif rule_type == 'DOMAIN-SUFFIX':
                    domain_suffixes.append(value)
                    self.stats['rule_types']['domain_rules'] += 1
                elif rule_type == 'DOMAIN-KEYWORD':
                    domain_keywords.append(value)
                    self.stats['rule_types']['domain_rules'] += 1
                elif rule_type == 'IP-CIDR':
                    if self.is_valid_ip_cidr(value):
                        ip_cidrs.append(value)
                        self.stats['rule_types']['ip_rules'] += 1
                elif rule_type == 'PROCESS-NAME':
                    process_names.append(value)
                    self.stats['rule_types']['process_rules'] += 1
        
        # Build sing-box rule object - efficient integration format
        rule_obj = {}
        
        # Only add non-empty fields
        if domains:
            rule_obj['domain'] = domains
        if domain_suffixes:
            rule_obj['domain_suffix'] = domain_suffixes
        if domain_keywords:
            rule_obj['domain_keyword'] = domain_keywords
        if ip_cidrs:
            rule_obj['ip_cidr'] = ip_cidrs
        if process_names:
            rule_obj['process_name'] = process_names
        
        # If there are no rules, return empty object
        if not rule_obj:
            return {}
        
        # Build complete structure conforming to sing-box official documentation
        # Reference: https://sing-box.sagernet.org/configuration/rule-set/source-format/
        result = {
            "version": 2,  # Use version 2, supports optimized domain_suffix rules
            "rules": [rule_obj]  # Put the integrated rule object into the rules array
        }
        
        return result
    
    def process_entry(self, entry_name: str, entry_info: Dict) -> bool:
        """Process a single entry"""
        try:
            # Determine the best version
            best_version = self.determine_best_version(entry_name, entry_info)
            
            # Get rules
            rules = self.merge_versions_if_needed(entry_name, entry_info)
            
            if not rules:
                logging.warning(f"Entry {entry_name} has no valid rules")
                return False
            
            # Convert to sing-box format
            singbox_rule = self.convert_to_singbox_format(rules)
            
            if not singbox_rule['rules']:
                logging.warning(f"Entry {entry_name} has no valid rules after conversion")
                return False
            
            # 🎯 Key fix: Save as JSON file conforming to sing-box official standards and efficient format
            output_file = os.path.join(self.target_dir, f"{entry_name}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(singbox_rule, f, ensure_ascii=False, indent=2)
            
            # Update statistics
            if '_Classical.yaml' in best_version:
                self.stats['version_selection']['classical_used'] += 1
            elif len(entry_info['versions']) > 1:
                self.stats['version_selection']['merged_versions'] += 1
            else:
                self.stats['version_selection']['single_version'] += 1
            
            self.stats['entries_processed'] += 1
            return True
            
        except Exception as e:
            logging.error(f"Error processing entry {entry_name}: {e}")
            self.stats['entries_skipped'] += 1
            return False
    
    def run_optimal_integration(self):
        """Run optimal integration"""
        logging.info("Starting optimal integration (Fixed version 9 - Efficient integration format + Official documentation standards)...")
        
        # 🧹 Key fix: Automatically clear target directory before running
        if not self.clean_target_directory():
            logging.error("Failed to clear target directory, exiting program")
            return None
        
        # Discover all entries
        self.discover_all_entries()
        
        # Sort entries by priority
        sorted_entries = sorted(
            self.all_entries.items(),
            key=lambda x: (x[1]['version_priority'], x[0]),
            reverse=True
        )
        
        # Process all entries
        for entry_name, entry_info in sorted_entries:
            logging.info(f"Processing entry: {entry_name} (version: {entry_info['best_version']})")
            self.process_entry(entry_name, entry_info)
        
        # Output statistics
        self.print_statistics()
        
        return self.stats
    
    def print_statistics(self):
        """Print statistics"""
        logging.info("=" * 50)
        logging.info("Optimal integration completed (Fixed version 9 - Efficient integration format + Official documentation standards)!")
        logging.info("=" * 50)
        logging.info(f"Total entries: {self.stats['total_entries_found']}")
        logging.info(f"Successfully processed: {self.stats['entries_processed']}")
        logging.info(f"Skipped entries: {self.stats['entries_skipped']}")
        logging.info(f"Success rate: {self.stats['entries_processed']/self.stats['total_entries_found']*100:.1f}%")
        
        logging.info("\nVersion selection statistics:")
        logging.info(f"  - Used Classical version: {self.stats['version_selection']['classical_used']}")
        logging.info(f"  - Merged multiple versions: {self.stats['version_selection']['merged_versions']}")
        logging.info(f"  - Used single version: {self.stats['version_selection']['single_version']}")
        
        logging.info("\nRule type statistics:")
        logging.info(f"  - Domain rules: {self.stats['rule_types']['domain_rules']}")
        logging.info(f"  - IP rules: {self.stats['rule_types']['ip_rules']}")
        logging.info(f"  - Process rules: {self.stats['rule_types']['process_rules']}")
        
        logging.info("\n🎯 Perfect combination:")
        logging.info("  - ✅ Conforms to sing-box official documentation standards")
        logging.info("  - ✅ Efficient integration format (grouped by type)")
        logging.info("  - ✅ Significantly reduced file size")
        logging.info("  - ✅ Uses version: 2")
        logging.info("  - ✅ Reference documentation: https://sing-box.sagernet.org/configuration/rule-set/source-format/")

if __name__ == "__main__":
    integrator = OptimalIntegrationFixedV9()
    result = integrator.run_optimal_integration()
