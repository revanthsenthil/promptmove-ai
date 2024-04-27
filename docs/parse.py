import json

def get_licenses(sbom_file):
    licenses = set()

    with open(sbom_file) as f:
        sbom = json.load(f)

    for component in sbom.get('components', []):
        licenses_info = component.get('licenses', [])

        for license_info in licenses_info:
            if 'license' in license_info:
                license_name = license_info['license'].get('name')
                if license_name is not None and 'declared' not in license_name:
                    licenses.add(license_name)
            elif 'licenses' in license_info:
                licenses_list = license_info['licenses']
                for license_dict in licenses_list:
                    license_name = license_dict.get('name')
                    if license_name is not None and 'declared' not in license_name:
                        licenses.add(license_name)
            if 'license' in license_info:
                license_name = license_info['license'].get('id')
                if license_name is not None and 'declared' not in license_name:
                    licenses.add(license_name)
            elif 'licenses' in license_info:
                licenses_list = license_info['licenses']
                for license_dict in licenses_list:
                    license_name = license_dict.get('id')
                    if license_name is not None and 'declared' not in license_name:
                        licenses.add(license_name)

    return licenses

sbom_file = 'promptmove.bom'
licenses = get_licenses(sbom_file)
print(licenses)