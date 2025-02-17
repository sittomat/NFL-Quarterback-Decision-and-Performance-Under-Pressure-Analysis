QB Pressure Analysis

Requirements
Python 3.10
Numpy 1.24.3
Pandas 2.0.2
Altair 5.0.1
Scikit-learn 1.2.2

Install these libraries and its dependencies with the following command: pip install -r requirements.txt

Make sure the following CSV files are in the data folder:
games.csv
player_play.csv
players.csv
plays.csv

Python Script Overview
process_qb_pressure.py extracts and analyzes plays where quarterbacks face defensive pressure in NFL games. It processes data from multiple CSV files and filters plays to identify quarterback performance under pressure, or not under pressure, and returns the dataset.

The returned dataset contains the following columns:
gameId: Unique identifier for each NFL game.
playId: Unique identifier for each play within a game.
game_play_id: gamedId and playId concatenated.
scoreDelta: The score difference at the time of the play. The difference represents the player's team points total minus the opponent's point total
displayName: Name of the player involved in the play.
down: The current down (1st, 2nd, 3rd, or 4th) at the start of the play.
yardsToGo: The number of yards needed to achieve a first down.
absoluteYardLineNumber: Distance from end zone for possession team. For example, this value is 30 if the possession team is on the 30 yard line on their half of the field. If on the opponent's 30 yard line, the absoluteYardLineNumber will be 70. 
passResult: Outcome of the pass (e.g., complete, incomplete, interception).
prePenaltyYardsGained: Total yards gained on the play not including penalties.
passLength: Distance of the pass attempt in the air.
timeToThrow: Time elapsed from snap to pass release.
timeInTackleBox: Time the quarterback spent inside the tackle box.
hadRushAttempt: Indicates whether the quarterback attempted a rushing play.
rushingYards: Number of yards gained on a quarterback rush.
qbSneak: Indicates if the quarterback executed a sneak play.
qbKneel: Indicates if the quarterback performed a kneel-down.
qbSpike: Indicates if the quarterback spiked the ball to stop the clock.
passingYards: Total passing yards gained on the play.


Features
Loads and merges game, player, and play data.
Identifies plays where defensive pressure was applied, and plays where defensive pressure was not applied.
Filters out non-QB players and duplicate entries.
Removes any plays with any incorrect QB entries. These will be trick plays where the QB assigned on the play is not actually a quarterback, but plays a different position. 
Create scoreDelta column in the dataset that shows the difference of scores at the time of the play.
Cleans and structures the dataset for further analysis.
Runs the process_qb_pressure_data function in process_qb_pressure.py, and generates datasets for QB pressure and QB non-pressure data entries. Both are exported to separate CSV files. 

Usage
Run the script using:
python process_qb_pressure.py


Output
The script outputs a filtered dataset of quarterback plays under pressure, ready for further analysis or modeling.



Python Notebook Overview
The qb_pressure_analysis.ipynb Python Notebook uses the pressure and no pressure datasets formed by the process_qb_pressure_data() function to create new tables and visualizations for our analysis. 

Here is an overview of all that was done in the Python Notebook file:
Load the pressure and no pressure datasets using the process_qb_pressure_data() function

There were many plays where the passResult was NULL. To fix this, a playType column was made for each dataset. The value is 1 of 2: Pass or Scramble. Pass was assigned to plays with a passResult that is either C(complete pass), IN(incomplete pass), I(interception), or S(sack). Scramble was assigned to plays where passResult is R(scramble) or hadRushAttempt is 1, meaning a run happened. Additionally, a passResultLong variable was also created. This passResultLong will be a more descriptive description of passResult. Here is the following mapping from passResult to passResultLong: C --> Complete Pass, I --> Incomplete Pass, S --> QB Sack, R --> Scramble, IN --> Interception. This is outlined in the set_playType() function. Only the dataframe(either the pressure or no pressure data) is passed into this function. 

Created a function create_bar_chart() that would create an Altair bar chart given a dataframe. The function's required arguments are as follows: the dataframe being used, x-axis column, y-axis column, bar labels, and chart title. The optional arguments include the following: max value for y-axis scale, chart width, chart height, sort order, label angle, and label size. The dataframe being fed into this function will be a condensed version of pressure and/or non-pressure data. Here are the following bar charts created using this function:
1. Scramble Rate (Pressure vs No Pressure)
2. Scramble Rate by Down(QB Under Pressure)
3. Scramble Rate by Down(QB Under No Pressure)
4. Distribution of Passing Play Results (QB Under Pressure)
5. Distribution of Passing Play Results (QB Under No Pressure)
6. Average Pre-Penalty Yards by Quarterback(QB Under Pressure)
7. Average Completion Percentage by Quarterback(QB Under Pressure)
8. Average Pre-Penalty Yards by Quarterback(QB Under No Pressure)
9. Average Completion Percentage by Quarterback(QB Under No Pressure)

Created a function create_grouped_bar_chart() that would create an Altair grouped bar chart given parameters. The function's required arguments are as follows: the dataframe being used, column name for main categories(specified in legend of chart what category each color represents), column name for group(what each group of colored bars belongs to), column name for y-axis values, and chart title. The optional arguments include the following: max value for y-axis scale, chart width, chart height, and sort order. The dataframe being fed into this function will be a condensed version of pressure and/or non-pressure data. Here are the following bar charts created using this function:
1. Average Yards Gained by Play Type - average yards gained by Pass or Scrambles in Pressure or Non-Pressure situations

Created a function create_histogram() that creates an overlayed Altair histogram given parameters. The function's required arguments are as follows: the dataframe being used, column name for values to distribute, chart title, and chart subtitle. The optional arguments are as follows: secondary data to plot, specified number of bins in histogram, width of histogram, and height of histogram. The dataframe being fed into this function will be a condensed version of pressure and/or non-pressure data. The plot will have the primary data's bins in blue(pressure data), and it will be overlayed with the secondary data's bins with a dashed black outline(non-pressure data). A red line will also be placed to represent the true average of the column values to distribute. Here are the following histograms created using this function:
1. Distribution of Yards to First Down
2. Distribution of Score Delta
3. Distribution of Yards to Endzone
4. Distribution of Pass Length
5. Distribution of Pass Length Resulting in Interceptions

Created a function create_QB_summary() that creates a dataframe of player by player summary statistics for a specific passResult type. The parameters are as follows: the dataframe with all player data(pressure or no pressure dataset), the string representing the passResult parameter('C', 'IN', 'R', or 'S'), and the name of the yards column to average(optional). This will be run for the pressure and non-pressure datasets, for each passResult type. In the end, all 4 pressure summaries are merged into one, and all 4 non-pressure summaries are merged into one.

Charts 6 and 7 in the create_bar_chart() section are then created with the pressure data large summary. The quarterbacks are sorted by highest pre-penalty yard average (or completion percentage) in descending order, with the quarterback names populating the x-axis, and the yard average (or completion percentage) populating the y-axis. The yard average (or completion percentage) is also written above each bar, representing its value. Charts 8 and 9 were similarly created, only using the non-pressure large summary. 

Using these two player by player summaries, a function create_scatter() was created to print scatterplots for a player by player visualization. The function's required arguments are as follows: the dataframe being used, column name for x-axis data, and column name for y-axis data. The optional arguments are as follows: column name for text labels, column names to include in tooltip, chart title, x-axis title, y-axis title, minimum value for x-axis, maximum value for x-axis, minimum value for y-axis, maximum value for y-axis, width of chart, and height of chart. The dataframe input into this function is one of the pressure or non-pressure summaries generated by the create_QB_summary() function, filtered by quarterbacks with at least 30 snaps under pressure. Here are the two scatter plots generated by this function:
1. Scramble Rate vs. Average Pre-Penalty Yards (QB Under Pressure)
2. Scramble Rate vs. Average Pre-Penalty Yards (QB Under No Pressure)
3. Pre-Penalty Yards Gained by QB - Under Pressure vs. No Pressure
4. Completion % by QB - Under Pressure vs. No Pressure

Each scatter plot will have a point representing each quarterback. The quarterback's last name will be to the right of that point, so you can immediately know where each quarterback is on the graph. 

Additionally, a linear regression line was added to each scatter plot. The created function get_linear_fit_chart() is used to create the linear regression line, and this is added to each scatter plot. The arguments are as follows: Dataset to use in linear regression line fit(quarterback pressure or no pressure summary), Column name for x-axis data, Column name for y-axis data, and Opacity of output line(optional). 

Finally, the correlation between pressure and non-pressure data was calculated, specifically for average total yards gained and completion percentage. 

Usage
In the qb_pressure_analysis.ipynb file, simply click Run on all cells you want to run


Output
All generated dataframes and visualizations will be made after the conclusion of its code cell execution.
