import os
import shutil
from datetime import datetime

def migrate_data():
    """Migrate existing data files to new directory structure"""
    old_data_dir = 'trending_data'
    
    # Get all existing json files
    old_files = [f for f in os.listdir(old_data_dir) if f.endswith('.json')]
    
    for old_file in old_files:
        # Parse date from filename (format: YYYY-MM-DD.json)
        date_str = old_file[:-5]  # Remove .json
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            year = date_obj.strftime('%Y')
            month = date_obj.strftime('%m')
            day = date_obj.strftime('%d')
            
            # Create new directory structure
            new_year_dir = os.path.join(old_data_dir, year)
            new_month_dir = os.path.join(new_year_dir, month)
            os.makedirs(new_month_dir, exist_ok=True)
            
            # Move file
            old_path = os.path.join(old_data_dir, old_file)
            new_path = os.path.join(new_month_dir, f'{day}.json')
            
            if not os.path.exists(new_path):
                shutil.move(old_path, new_path)
                print(f'Moved {old_file} to {new_path}')
            else:
                print(f'File {new_path} already exists, skipping {old_file}')
                
        except ValueError as e:
            print(f'Error parsing date from {old_file}: {e}')
            continue

if __name__ == '__main__':
    migrate_data()
    print('Migration completed!') 