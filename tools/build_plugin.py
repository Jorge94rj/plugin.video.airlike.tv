from create_zip_file import create_zip_file, get_zip_file_name

output_file_name = get_zip_file_name()

print(f"Creating zip file {output_file_name}")
create_zip_file()
print(f"{output_file_name} file finished")
