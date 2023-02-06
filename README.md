# congressman-donation-scraper
This project scrapes the website opensecrets.org to obtain contribution records for each senator.

Functions: 
  get_congresspeople: 
    Using the url of the alphabeitical list of current congresspeople
    (https://www.opensecrets.org/members-of-congress/members-list?cong_no=117&cycle=2020),
    this function creates a dictionary of all the congresspeople and the link to their profile pages. 
  
  get_contributors: 
    Using the url to a congressperson's profile page, this function returns a 
    dictionary of every top donator over a congressman's career and the amount they donated. 
    
  get_totals:
    Using the get_congresspeople, this function scrapes every congressperson's top donators and creates
    a dictionary of all donators and their total donations. 

  sort_dict:
    Sorts a given dictionary in descending or nondescending order. 
    
   write_csv:
    Writes a given dictionary to a csv file. The function also takes in a string for the filename. 
