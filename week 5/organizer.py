import os
import shutil
import json
from datetime import datetime

CATEGORY_MAP = {
	'documents': ['.pdf', '.docx', '.txt'],
	'images': ['.png', '.jpg', '.jpeg', '.JPG'],
	'archives': ['.zip', '.tar.gz', '.tar', '.gz'],
	'executables': ['.exe', '.sh', '.bat', '.msi'],
	'videos': ['.mp4', '.avi', '.mov'],
	'audio': ['.mp3', '.wav', '.aac'],
}

OTHER_CATEGORY = 'other'

def get_category(filename):
	ext = os.path.splitext(filename)[1].lower()
	for category, extensions in CATEGORY_MAP.items():
		if ext in extensions:
			return category
	return OTHER_CATEGORY

def organize_files(source_dir):
	summary = {
		'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p'),
		'source_directory': os.path.abspath(source_dir),
		'total_files': 0,
		'categories': {cat: 0 for cat in CATEGORY_MAP.keys()},
		OTHER_CATEGORY: 0,
		'organized_files': 0,
		'errors': [],
		'warnings': []
	}
	files = []
	for entry in os.listdir(source_dir):
		path = os.path.join(source_dir, entry)
		if os.path.isfile(path):
			files.append(entry)
	summary['total_files'] = len(files)

	for filename in files:
		category = get_category(filename)
		dest_folder = os.path.join(source_dir, category)
		if not os.path.exists(dest_folder):
			try:
				os.makedirs(dest_folder)
			except Exception as e:
				summary['errors'].append(f"Failed to create folder: {dest_folder} ({e})")
				continue
		src_path = os.path.join(source_dir, filename)
		dest_path = os.path.join(dest_folder, filename)
		try:
			shutil.move(src_path, dest_path)
			summary['categories'][category] = summary['categories'].get(category, 0) + 1
			summary['organized_files'] += 1
		except Exception as e:
			summary['errors'].append(f"Failed to move {filename}: {e}")

	return summary

def generate_reports(summary, output_dir):
	json_path = os.path.join(output_dir, 'organization_report.json')
	json_report = {
		"generated": summary['timestamp'],
		"source_directory": summary['source_directory'],
		"summary": {
			"total_files": summary['total_files'],
			"organized_files": summary['organized_files'],
			"errors_count": len(summary['errors']),
			"warnings_count": len(summary['warnings'])
		},
		"categories": [
			{
				"name": cat.upper(),
				"count": count,
				"percent": round((count / summary['total_files'] * 100) if summary['total_files'] else 0, 1)
			} for cat, count in summary['categories'].items()
		] + [
			{
				"name": OTHER_CATEGORY.upper(),
				"count": summary[OTHER_CATEGORY],
				"percent": round((summary[OTHER_CATEGORY]/summary['total_files']*100) if summary['total_files'] else 0, 1)
			}
		],
		"errors": summary['errors'],
		"warnings": summary['warnings']
	}
	with open(json_path, 'w') as f:
		json.dump(json_report, f, indent=4)

	txt_path = os.path.join(output_dir, 'organization_report.txt')
	with open(txt_path, 'w') as f:
		f.write('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n')
		f.write('FILE ORGANIZATION REPORT\n')
		f.write('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n')
		f.write(f"Generated: {summary['timestamp']}\n")
		f.write(f"Source Directory: {summary['source_directory']}\n\n")
		f.write('SUMMARY\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n')
		f.write(f"Total Files Found: {summary['total_files']}\n")
		f.write(f"Successfully Organized: {summary['organized_files']}\n")
		f.write(f"Errors: {len(summary['errors'])}\n\n")
		f.write('CATEGORIES\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n')
		for cat, count in summary['categories'].items():
			percent = (count / summary['total_files'] * 100) if summary['total_files'] else 0
			f.write(f"{cat.upper():12}: {count} file{'s' if count != 1 else ''} ({percent:.1f}%)\n")
		other_count = summary[OTHER_CATEGORY]
		other_percent = (other_count / summary['total_files'] * 100) if summary['total_files'] else 0
		f.write(f"{OTHER_CATEGORY.upper():12}: {other_count} file{'s' if other_count != 1 else ''} ({other_percent:.1f}%)\n\n")
		f.write('ERRORS & WARNINGS\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n')
		for err in summary['errors']:
			f.write(f"{err}\n")
		for warn in summary['warnings']:
			f.write(f"{warn}\n")
		f.write('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n')
		f.write('Organization complete!\n')

if __name__ == '__main__':
	from pathlib import Path
	source_dir = r"e:\python_basics\week 5\test_downloads"
	print(f"Scanning directory: {source_dir}")
	if not os.path.isdir(source_dir):
		print(f"Directory '{source_dir}' does not exist or is not accessible. Exiting.")
		exit(1)
	summary = organize_files(source_dir)
	generate_reports(summary, source_dir)
