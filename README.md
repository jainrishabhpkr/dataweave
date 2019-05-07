# datawaeve



As the json file provided has multiple json objects in multiple line. we parsed it line by line as seperate dictinaries.Firstly imported json module to use methods to convert json into python dictionaries. created two empty lists data_yesterday and data_today and used it to store the respective json objects as list item thereby creating lists of dictionary where each list item is a dictionary


1. created three empty sets urlh_set_yesterday, urlh_set_today, urlh_set_common where  urlh_set_yesterday, urlh_set_today are used to store distinct urlh values retreived from dictionary using lisitem.get('urlh').
To get overlapping of urlh we use intersection of two sets


2. created two empty dictionaries to store available price of respective urlh.
we run a for loop through data_today and data_yesterday. we selected only those json objects whose urlh is in urlh_set_common and http_status=200 and price is not None.
creat another dictionary price_difference where key is urlh and values are price difference. we use absolute to get positive difference



3. created two sets categories_today and categories_yesterday to add unique category to each . to get unique categories from both files we applied union operation to categories_today and categories_yesterday. also create a set called subcategory_both to add subcategories from both files



4. To get list of categories which is not overlapping we use symmetric difference or difference two times. once (categories_today-categories_yesterday )and other (categories_yesterday-categories_today)



5. create a set categories_both to store all categories. run a for loop through categories_both. in each iteration run a for loop through subcategory_both. there we check in each json object for the combination of category and subcategory and update the count if found 1 and add the count as value and category + ">" + subcategory as key in taxonomy


6. Firstly we get maximum mrp from each files.then we craete normalized_data_today and normalized_data_yesterday to store the noramlized results. we loop trhough each json objects and change the value of mrp where it was None or 0 to NA. to noramalize it we divided mrp wit max_mrp.
