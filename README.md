# Work Log
In order to prepare better timesheets for your company, you've been asked to develop a terminal application for logging what work someone did on a certain day. The script should ask for a task name, how much time was spent on the task, and any general notes about the task. Record each of these items into a row of a CSV or JSON file along with a date.

Provide a way for a user to find all of the tasks that were done on a certain date or that match a search string (either as a regular expression or a plain text search). Print a report of this information to the screen, including the date, title of task, time spent, and general notes.

Make sure your script runs without errors. Catch exceptions and report errors to the user in a meaningful way.
As a user of the script, I should be prompted with a menu to choose whether to add a new entry or lookup previous entries.
As a user of the script, if I choose to enter a new work log, I should be able to provide a task name, a number of minutes spent working on it, and any additional notes I want to record.
As a user of the script, if I choose to find a previous entry, I should be presented with four options:
find by date
find by time spent
find by exact search
find by pattern

Menu has a “quit” option to exit the program.
Entries can be deleted and edited, letting user change the date, task name, time spent, and/or notes.
Entries can be searched for and found based on a date range. For example between 01/01/2016 and 12/31/2016.
Entries are displayed one at a time with the ability to page through records (previous/next/back).
