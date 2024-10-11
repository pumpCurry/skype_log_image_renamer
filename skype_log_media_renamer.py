import sys
# sys.path.append('C:\\something\\site-packages')
import os
import shutil
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

# skype log image renamer (C) pumpcurry 2024

def parse_date(date_str):
    # 日付文字列が7桁のミリ秒を持っている場合、6桁にトリム
    if date_str.endswith('Z'):
        parts = date_str[:-1].split('.')
        if len(parts) > 1 and len(parts[1]) > 6:
            date_str = parts[0] + '.' + parts[1][:6] + 'Z'
    
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%f%z"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data '{date_str}' does not match any expected format")

def adjust_date_if_needed(date_str):
    file_date = parse_date(date_str)
    if file_date.year > 3000:
        adjusted_date = file_date - relativedelta(years=1000, months=4, days=1)
        return adjusted_date
    return file_date

def process_files(target_folder, processed_folder, copy_folder, timezone):
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
    if not os.path.exists(copy_folder):
        os.makedirs(copy_folder)

    for filename in os.listdir(target_folder):
        if filename.endswith('.json'):
            json_path = os.path.join(target_folder, filename)
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if 'expiry_date' exists in JSON
                if 'expiry_date' not in data:
                    print(f"Key 'expiry_date' not found in {json_path}")
                    continue
                
                # Extract the date and filename from JSON
                timestamp = data['expiry_date']
                original_filename = data.get('filename', 'default_filename.ext')  # default filename if not present
                
                try:
                    file_date = parse_date(timestamp)
                except ValueError:
                    print(f"Failed to parse date normally, adjusting: {timestamp}")
                    file_date = adjust_date_if_needed(timestamp)
                
                # Adjust date if beyond 3000 and add 1 day
                if file_date.year > 3000:
                    file_date = file_date - relativedelta(years=1000, months=4) + timedelta(days=1)
                
                # Convert to specified timezone
                file_date = file_date.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(timezone))
                formatted_date = file_date.strftime("%Y-%m-%d_%H-%M-%S-%fZ")

                # Find the associated media file
                base_name = os.path.splitext(filename)[0]
                media_files = [f for f in os.listdir(target_folder) if f.startswith(base_name) and not f.endswith('.json')]
                if not media_files:
                    print(f"No associated media file found for {json_path}")
                    continue
                
                # Process each associated media file
                for media_file in media_files:
                    media_path = os.path.join(target_folder, media_file)
                    
                    # Extract the extension part from the original filename
                    ext = os.path.splitext(media_file)[1]
                    # Check if the file has an additional numeric suffix
                    suffix = ''
                    parts = media_file.split('.')
                    if len(parts) > 2 and parts[-2].isdigit():
                        suffix = f"_{parts[-2]}"
                    
                    new_filename = formatted_date + suffix + ext
                    new_path = os.path.join(copy_folder, new_filename)
                    shutil.copy2(media_path, new_path)
                    print(f"Copied {media_path} to {new_path}")

                # Move the processed files to the processed folder
                shutil.move(json_path, os.path.join(processed_folder, filename))
                for media_file in media_files:
                    shutil.move(os.path.join(target_folder, media_file), os.path.join(processed_folder, media_file))
            except Exception as e:
                print(f"Failed to process {json_path}: {e}")
                continue

if __name__ == "__main__":
    default_target_folder = "./media" if os.name != 'nt' else ".\\media"
    default_processed_folder = "./media_old" if os.name != 'nt' else ".\\media_old"
    default_copy_folder = "./media_renamed" if os.name != 'nt' else ".\\media_renamed"
    
    target_folder = input(f"Enter the path to the target folder [{default_target_folder}]: ") or default_target_folder
    processed_folder = input(f"Enter the path to the processed folder [{default_processed_folder}]: ") or default_processed_folder
    copy_folder = input(f"Enter the path to the copy folder [{default_copy_folder}]: ") or default_copy_folder
    
    # Get the local timezone, default to Asia/Tokyo if not found
    local_timezone = os.environ.get('TZ', 'Asia/Tokyo')
    
    try:
        local_timezone = pytz.timezone(local_timezone)
    except pytz.UnknownTimeZoneError:
        local_timezone = 'Asia/Tokyo'
    
    user_timezone = input(f"Enter the timezone [{local_timezone}]: ") or local_timezone
    
    process_files(target_folder, processed_folder, copy_folder, str(user_timezone))
