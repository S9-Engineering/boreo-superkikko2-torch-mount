#!/usr/bin/env python3
"""Build the allowlisted, unreleased R13 prototype printing package.

Required Notice: S9 Engineering (https://github.com/S9-Engineering)
SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
from pathlib import Path, PurePosixPath
import hashlib,json,re,zipfile

ROOT=Path(__file__).resolve().parents[2]
FOLDER=ROOT/'packages/r13-prototype'

def digest(data):return hashlib.sha256(data).hexdigest()

def main():
    recipe=json.loads((FOLDER/'manifest.json').read_text())
    assert recipe['status']=='UNRELEASED_PROTOTYPE'
    payload={};rows=[]
    for row in recipe['files']:
        source=ROOT/row['source'];name=row['archive'];dest=PurePosixPath(name)
        assert source.resolve().is_relative_to(ROOT) and source.is_file() and not source.is_symlink()
        assert 'publication-local' not in source.parts
        assert not dest.is_absolute() and '..' not in dest.parts and name not in payload
        assert row['role'] in ['model','instructions','image','license']
        content=source.read_bytes();payload[name]=content
        if 'expected_sha256' in row:assert digest(content)==row['expected_sha256'],name
        rows.append({**row,'sha256':digest(content),'bytes':len(content)})
    assert {'README.md','LICENSE.txt','LICENSE-SOFTWARE.txt','LICENSING.md'}<=payload.keys()
    assert len([n for n in payload if n.endswith('.stl')])==2
    assert len([n for n in payload if n.endswith('.3mf')])==1
    # Check standalone Markdown links against the archive rather than its parent repository.
    checked=[]
    for name,data in list(payload.items()):
        if not name.endswith('.md'):continue
        for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',data.decode()):
            if target.startswith(('https:','http:','mailto:')):continue
            from urllib.parse import unquote
            linked=PurePosixPath(name).parent/unquote(target)
            assert str(linked) in payload,(name,target)
            checked.append({'document':name,'target':str(linked)})
    metadata={'revision':'R13','status':recipe['status'],'files':rows,
      'geometry_or_slicing_changed':False,'physical_tests':False,'gcode':'Native 3MF contains the verified setup-specific embedded path; no standalone G-code selected.'}
    payload['manifest.json']=(json.dumps(metadata,indent=2)+'\n').encode()
    payload['SHA256SUMS.txt']=''.join(digest(data)+'  '+name+'\n' for name,data in sorted(payload.items())).encode()
    output=FOLDER/recipe['output']
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(payload.items()):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None and set(z.namelist())==set(payload)
        assert all(z.read(n)==data for n,data in payload.items())
    checksum=output.with_suffix('.zip.sha256');checksum.write_text(digest(output.read_bytes())+'  '+output.name+'\n')
    report={'status':'PASS','archive':str(output.relative_to(ROOT)),'sha256':digest(output.read_bytes()),
      'members':len(payload),'bytes':output.stat().st_size,'standalone_links':checked,'files':rows,
      'portal_files_included':False,'tag_or_release_created':False,'physical_tests':False}
    (FOLDER/'package-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','archive','members','bytes','sha256']}))

if __name__=='__main__':main()
