
import argostranslate.package

print("Checking available translation models...")

argostranslate.package.update_package_index()
packages = argostranslate.package.get_available_packages()

languages = [("en", "hi"), ("hi", "en")]

for from_code, to_code in languages:
    package = next(
        (
            p for p in packages
            if p.from_code == from_code
            and p.to_code == to_code
        ),
        None,
    )

    if package:
        print(f"Downloading {from_code} -> {to_code}...")
        download_path = package.download()
        argostranslate.package.install_from_path(download_path)
        print(f"Installed {from_code} -> {to_code}")
    else:
        print(f"Model unavailable: {from_code} -> {to_code}")

print("Finished installing available models.")
