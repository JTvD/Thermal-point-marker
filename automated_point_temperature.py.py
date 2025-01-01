"""Example off how to extract the temperature values of a list of points.
Saves the values in a dataframe/prints them."""
import cv2
import numpy as np
import pandas as pd
from pathlib import Path


class bulk_extraction():
    """ Class wrapper"""

    def __init__(self, csv_marker: str = '_thermal',
                 img_maker: str = '_falsecolor'):
        """ Initialize the class.
            args:
                img_makers: str, name conventon of the thermal images
                """
        self.csv_marker = csv_marker
        self. img_maker = img_maker

    def get_files(self, ff_path: Path):
        """Get all pairs of CSv files and images
            args:
                ff_path: Path object, path to the directory or file
            returns:
                dictionary of paths to the image and csv
        """
        # Get all CSV files in the directory or the file itself
        if ff_path.is_dir():
            csvs = list(ff_path.glob('*.csv'))
        elif ff_path.is_file() and ff_path.suffix == '.csv':
            csvs = [ff_path]
        else:
            csvs = []

        # Get the corresponding images
        files = []
        for csv_filename in csvs:
            img_filename = csv_filename.with_name(csv_filename.stem.
                                                  replace('_thermal',
                                                          '_falsecolor') +
                                                  '.png')
            if img_filename.exists():
                files.append({'thermal': csv_filename, 'image': img_filename})
        return files

    def get_temperature(self, to_analyse: Path,
                        point_list: list, mark_image: bool = False):
        """ Extract the temperature values of a list of predifined points.
            args:
                to_analyse: Path, image or folder to extract temperatures
                point_list: list, list of points to extract
                mark_image: bool, mark the points on the image
            returns:
                result_df: pd.DataFrame, dataframe with the temperature values
        """
        # White point with a black border
        white_color = (255, 255, 255)
        black_color = (0, 0, 0)

        # Get the files
        files = self.get_files(to_analyse)

        # Process files
        results_list = []
        for filepair in files:
            # Load temperature values
            temp_values = np.genfromtxt(filepair['thermal'], delimiter=',')
            one_file_dict = {
                'Source_file': filepair['thermal'].stem
            }

            # Load image?
            if mark_image:
                img = cv2.imread(filepair['image'])
            # Points are [X, Y], temperature values are Y, X
            for point in point_list:
                if mark_image:
                    cv2.circle(img, (point[0], point[1]), 1, white_color, -1)
                    cv2.circle(img, (point[0], point[1]), 2, black_color, 1)

                # Extract temperature
                temperature = temp_values[point[1]][point[0]]
                one_file_dict[f'{str(point[0])}_{str(point[1])}'] = temperature
                # print(f"xy: {point[0]}, {point[1]}, temp:{temperature}")
            results_list.append(one_file_dict)

            if mark_image:
                # Save the marked image
                img_path = filepair['image']
                img_path = img_path.with_name(img_path.stem +
                                              '_marked' +
                                              img_path.suffix)
                cv2.imwrite(img_path, img)

        # Combine all lists of dict into a dataframe
        result_df = pd.DataFrame(results_list)
        return result_df


if __name__ == "__main__":
    # List of points to mark: X,Y
    point_list = [[206, 74], [306, 100]]

    # Select image or folder to extract temperatures
    to_analyse = Path("test_data")
    # to_analyse = Path("test_data/e8xt_thermal.csv")

    # Get the temperature values
    processor = bulk_extraction()
    result_df = processor.get_temperature(to_analyse, point_list, True)

    print(result_df.head(5))
    # Print default statistics
    print(result_df.describe())

    # Save results as csv
    result_df.to_csv('point_temperature.csv', index=False)
