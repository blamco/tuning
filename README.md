# tuning
AMP Tuning tools

# Diag_analyzer.exe

Usage:
	Diag_analyzer.exe 
	- will use the first diagnostic in the directory alphabetically
	or
	Diag_analyzer.py Diagnostic_File.7z
	- will use the diagnostic file specified
	
Diag_analyzer.exe will check the provided AMP diagnostic file for sfc.exe.log files.  
It will then create a directory with the diagnostic file name and store the log files outside of the .7z.
Next, it will parse the logs and determine the Top 10 Processes, Files, Extensions and Paths.
Finally, it will print that information to the screen and also to a {Diagnostic}-summary.txt file.
