def filter_logs(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            lower_line = line.lower()
            if 'error' in lower_line and 'notice' not in lower_line:
                f_out.write(line)

if __name__ == "__main__":
    input_path = '/home/lenovo/Bureau/thesis-project/apache.log'
    output_path = 'apache_filtered.log'
    filter_logs(input_path, output_path)
