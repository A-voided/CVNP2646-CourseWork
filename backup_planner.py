import json, random, argparse

def load_config(path):
	try:
		with open(path) as f:
			return json.load(f)
	except Exception as e:
		return {'_load_error': str(e)}

def validate_config(cfg):
	errors = []
	if '_load_error' in cfg:
		errors.append(f"JSON load error: {cfg['_load_error']}")
	if not isinstance(cfg, dict):
		errors.append('Config must be a dict')
	if 'plans' not in cfg or not isinstance(cfg['plans'], list):
		errors.append('Missing/invalid plans')
	else:
		for idx, p in enumerate(cfg['plans']):
			for k in ('name','sources','destination'):
				if k not in p:
					errors.append(f'Plan {idx+1} missing key: {k}')
			if 'sources' in p:
				if not isinstance(p['sources'], list):
					errors.append(f'Plan {idx+1} sources must be list')
				elif len(p['sources']) == 0:
					errors.append(f'Plan {idx+1} sources list is empty')
				else:
					for sidx, src in enumerate(p['sources']):
						if isinstance(src, dict) and 'path' not in src:
							errors.append(f'Plan {idx+1} Source {sidx+1} missing path field')
						elif isinstance(src, str) and not src:
							errors.append(f'Plan {idx+1} Source {sidx+1} path is empty')
	return (len(errors)==0, errors)

def simulate_backup(cfg):
	results = []
	for p in cfg['plans']:
		sources = []
		total_files = 0
		total_size = 0
		for idx, src in enumerate(p['sources']):
			num_files = random.randint(5,15)
			files = [f"{src}/file{random.randint(1,100)}.dat" for _ in range(num_files)]
			sizes = [round(random.uniform(1,100),1) for _ in range(num_files)]
			total_files += num_files
			total_size += sum(sizes)
			sources.append({
				'name': f'SOURCE {idx+1}',
				'path': src,
				'files': files,
				'sizes': sizes,
				'num_files': num_files
			})
		results.append({
			'name': p['name'],
			'sources': sources,
			'dest': p['destination'],
			'total_files': total_files,
			'total_size': total_size
		})
	return results

def generate_report(results, out_path):
	sep = '+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+\n'
	import sys
	config_path = sys.argv[1] if len(sys.argv) > 1 else 'backup_config.json'
	try:
		with open(config_path) as meta_f:
			meta_cfg = json.load(meta_f)
	except Exception:
		meta_cfg = {}
	version = meta_cfg.get('version', '1.0')
	created_by = meta_cfg.get('created_by', 'security_team')
	with open(out_path,'w', encoding='utf-8') as f:
		f.write('              BACKUP PLAN DRY-RUN SIMULATION\n'+sep)
		for r in results:
			f.write(f"Plan: {r['name']}\nVersion: {version}\nCreated By: {created_by}\nMode: DRY-RUN (no files will be copied)\n{sep}")
			f.write('SUMMARY STATISTICS\n'+sep)
			f.write(f"Total Sources:     {len(r['sources'])}\n")
			f.write(f"Total Files:       {r['total_files']}\n")
			f.write(f"Total Size:        {round(r['total_size'],1)} MB\n")
			f.write(f"Destination:       {r['dest']}\n{sep}")
			for s in r['sources']:
				f.write(f"{s['name']}:\n{sep}")
				f.write(f"Path: {s['path']}\n")
				f.write(f"Files Found: {s['num_files']}\n\nSample Files:\n")
				for i in range(min(3, s['num_files'])):
					fname = s['files'][i].split('/')[-1]
					fsize = s['sizes'][i]
					f.write(f"  → {fname} ({fsize} MB)\n")
				if s['num_files'] > 3:
					f.write(f"  ... and {s['num_files']-3} more files\n")
				f.write(f"\n{sep}")
			f.write("This was a Dry-Run simulation. No files were copied or modified.\nTo execute actual backup, run with --execute flag.\n"+sep)

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('config')
	ap.add_argument('--output',default='sample_report.txt')
	args = ap.parse_args()
	cfg = load_config(args.config)
	valid, errors = validate_config(cfg)
	results = []
	if valid:
		results = simulate_backup(cfg)
		generate_report(results, args.output)
	print('\nValidation and runtime errors:')
	if errors:
		for e in errors:
			print('  -', e)
	else:
		print('  None')

if __name__ == '__main__':
	main()
