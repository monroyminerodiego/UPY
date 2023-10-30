# Linear Regression Simple Script  
## Instructions given by teacher  
Remember that this script must be a Script with a class called Linear Regression. This class must contain all methods and every method must be developed based on every step for the linear regression exercise shown in class. 

## Development  
In order to accomplish this task we created a class in 'simple.py', which has the following structure:
<table style="text-align:center;">
    <tr>
        <th style="text-align:center;"> Name </th>
        <th style="text-align:center;"> Type </th>
        <th style="text-align:center;"> Inputs </th>
        <th style="text-align:center;"> Outputs </th>
        <th style="text-align:center;"> Description </th>
    </tr>
    <tr>
        <td> generate_full_matrix </td>
        <td> Private </td>
        <td> - basic_matrix [list]: Expects a list with 'x' and 'y' values arranged in an iterable object. Eg: [ [1,2],[2,3],...,[6,7] ] </td>
        <td> Returns a DataFrame with 4 columns: 'x', 'y', 'x^2' and 'xy'. And their respective value </td>
        <td> Private function to generate a pandas DataFrame with the information and necessary columns to be used as guide to realize the simple linear regression. </td>
    </tr>
    <tr>
        <td> generate_sumatories </td>
        <td> Private </td>
        <td> Expects nothing </td>
        <td> - Returns the sumatory values of columns: x, y, xx and xy. (Following that specific order) </td>
        <td> Private function to generate the sumatories of the columns of 'full_matrix' DataFrame </td>
    </tr>
    <tr>
        <td> get_relevant_values </td>
        <td> Private </td>
        <td> Expects nothing </td>
        <td> Returns n(number of observations), m(slope of the line), b(intercept) and y(slope-intercept) values following that specific order </td>
        <td> Private function to get relevant values of the pandas DataFrame, such as: number of observations, slope of the line, intercept and the slope-intercept values </td>
    </tr>
    <tr>
        <td> get_predictions </td>
        <td> Private </td>
        <td> Expects nothing. </td>
        <td> Returns bb(sum of the squares of the residuals), m(Error of slope), b(error of intercept) values following that specigic order. </td>
        <td> Private function to calculate the predictions using the minimum square method. </td>
    </tr>
    <tr>
        <td> generate_plot </td>
        <td> Public </td>
        <td> Expects nothing. </td>
        <td> Returns nothing, but generates a window with the plot. </td>
        <td> Funtion to plot the scatter plot with the data of 'full_matrix' and it's relevant data. </td>
    </tr>
</table>

## Made By
- Juan Antonio Cel Vazquez
- Sergio Johanan Barrera Chan
- Ariel Joel Buenfil Góngora
- Diego Monroy Minero