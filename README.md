# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)


import pandas as pd

# Reading the Excel files into DataFrames
df1 = pd.read_excel('path_to_excel_file_1.xlsx')
df2 = pd.read_excel('path_to_excel_file_2.xlsx')

# Dropping rows with any null values in the entire DataFrame
df1_clean = df1.dropna()
df2_clean = df2.dropna()

# List of required columns for comparison
required_columns = ['column_name1', 'column_name2']  # Replace with actual column names

# Merging DataFrames on required columns to find common data
common_data = pd.merge(df1_clean, df2_clean, on=required_columns)

# Finding non-common data
non_common_df1 = df1_clean[~df1_clean[required_columns].apply(tuple, axis=1).isin(df2_clean[required_columns].apply(tuple, axis=1))]
non_common_df2 = df2_clean[~df2_clean[required_columns].apply(tuple, axis=1).isin(df1_clean[required_columns].apply(tuple, axis=1))]

# Printing common data
print("Common data based on required columns:")
print(common_data)

# Printing non-common data with highlighting
print("\nData in df1 not in df2:")
print(non_common_df1.style.set_properties(**{'background-color': 'yellow'}))

print("\nData in df2 not in df1:")
print(non_common_df2.style.set_properties(**{'background-color': 'yellow'}))