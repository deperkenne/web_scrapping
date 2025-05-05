from pathlib import Path

from coverage.types import FilePath

i = 0

# read all file that end with *.csv in specific path
def update_csv_file(path):
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"this {path} not exist")

    for file_csv in  path_obj.glob("*.csv"):
           read_line(file_csv)


# read line
def read_line(input_file):

    with open(input_file, "r", encoding="utf-8") as infile, open(f"{input_file}_update.csv", "w", encoding="utf-8") as outfile:
        for line in infile:
            try:
                index_col_subtitle_start = line.index('"')
                index_col_subtitle_end = line.index('",')
                index_col_description_start = line.index('"{')
                index_col_description_end = line.index('}"')
                index_col_images_start = line.index('"{',index_col_description_end+2,len(line))
                index_col_images_end = line.index('}"',index_col_description_end+2,len(line))
                substring_between_end_subtitle_and_start_description = line[index_col_subtitle_end+1:index_col_description_start].strip().replace(",", ";")
                substring_between_end_description_and_start_image = line[index_col_description_end + 1:index_col_images_start].strip().replace( ",", ";")
                substring_left_col_subtitle = line[0:index_col_subtitle_start].strip().replace(",", ";")
                substring_col_subtitle = line[ index_col_subtitle_start: index_col_subtitle_end+1]
                substring_col_description = line[index_col_description_start:index_col_description_end+2]
                substring_col_images = line[index_col_images_start:index_col_images_end+1]
                substring_right_col_images = line[index_col_images_end + 2:len(line)].strip().replace(",", ";")
                new_line =  substring_left_col_subtitle + substring_col_subtitle + substring_between_end_subtitle_and_start_description + substring_col_description +  substring_between_end_description_and_start_image + substring_col_images+ substring_right_col_images
                outfile.write(new_line + "\n")
            except FileNotFoundError:
                print("file not exist")
            except Exception:
                new_line = line.strip().replace(",", ";")
                outfile.write(new_line + "\n")
            finally:
                continue




if __name__ =="__main__":
    update_csv_file("CsvFiles")


