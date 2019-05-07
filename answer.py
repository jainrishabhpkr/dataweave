import json
data_yesterday, data_today = [], []
urlh_set_yesterday, urlh_set_today, urlh_set_common = set(), set(), set()
mini_yesterday, mini_today, price_difference = {}, {}, {}

with open('yesterday.json.gz_out') as f:
	for line in f:
		data_yesterday.append(json.loads(line))

with open('today.json.gz_out') as f:
	for line in f:
		data_today.append(json.loads(line))

for item in data_yesterday:
	urlh_set_yesterday.add(item.get('urlh'))

for item in data_today:
	urlh_set_today.add(item.get('urlh'))

# Q.1 No of URLH which are overlapping.

if ( urlh_set_yesterday & urlh_set_today ) :
	urlh_set_common = ( urlh_set_yesterday & urlh_set_today )
	print('No. of overlapping URLH : ', len(urlh_set_common))
else :
	print('There are no overlapping URLH')

# Q.2 For all the URLH which are overlapping, calculate the price difference (wrt available_price)
# if there is any between yesterday's and today's crawls. There might be duplicate URLHs in which
# case you can choose the first valid (with http_status 200) record.

temp_urlh_common = urlh_set_common.copy()
for item in data_yesterday:
	if item['urlh'] in temp_urlh_common and item['http_status'] == '200' and item['available_price'] != None:
		price = float(item['available_price'])
		mini_yesterday[item['urlh']] = price
		temp_urlh_common.remove(item['urlh'])

temp_urlh_common = urlh_set_common.copy()
for item in data_today:
	if item['urlh'] in temp_urlh_common and item['http_status'] == '200' and item['available_price'] != None:
		price = float(item['available_price'])
		mini_today[item['urlh']] = price
		temp_urlh_common.remove(item['urlh'])

for urlh in urlh_set_common :
	if urlh in mini_yesterday.keys() and urlh in mini_today.keys():
		price_difference[urlh] = abs(mini_yesterday[urlh] - mini_today[urlh])
print('Price Difference for overlapping URLHs : ')
print(price_difference)

# Q.3 No of Unique categories in both files.

categories_yesterday, categories_today, non_overlapping_categories, subcategory_both = set(), set(), set(), set()

for item in data_yesterday:
	categories_yesterday.add(item.get('category'))
	subcategory_both.add(item.get('subcategory'))

for item in data_today:
	categories_today.add(item.get('category'))
	subcategory_both.add(item.get('subcategory'))

print('No. of unique categories yesterday : ', len(categories_yesterday))
print('No. of unique categories today : ', len(categories_today))
print('No. of unique categories yesterday and today : ', len(categories_yesterday | categories_today))
print(categories_yesterday | categories_today)

# Q.4 List of categories which is not overlapping.

non_overlapping_categories.update(categories_yesterday - categories_today)
non_overlapping_categories.update(categories_today - categories_yesterday)
print(non_overlapping_categories)

# Q.5 Generate the stats with count for all taxonomies (taxonomy is concatenation of category and subcategory separated by " > ").

taxonomy = {}
categories_both = set()
categories_both.update(categories_yesterday)
categories_both.update(categories_today)
for category in categories_both:
	for subcategory in subcategory_both:
		count = 0
		for item in data_yesterday:
			if item['category'] == category and item['subcategory'] == subcategory:
				count += 1
		for item in data_today:
			if item['category'] == category and item['subcategory'] == subcategory:
				count += 1
		taxonomy_key = category + ' > ' + subcategory
		taxonomy[taxonomy_key] = count
print(taxonomy);


# Q.6 Generate a new file where mrp is normalized. If there is a 0 or a non-float value or the key doesn't exist, make it "NA".

# new_normalized_mrp = mrp_old / mrp_max

max_mrp = 0
temp_mrp = 0
for item in data_yesterday:
	if 'mrp' in item.keys() and item['mrp'] != None :
		temp_mrp = float(item['mrp'])
		max_mrp = max(max_mrp, temp_mrp)
for item in data_today:
	if 'mrp' in item.keys() and item['mrp'] != None :
		temp_mrp = float(item['mrp'])
		max_mrp = max(max_mrp, temp_mrp)
# print(max_mrp)

normalized_data_yesterday = data_yesterday.copy()
normalized_data_today = data_today.copy()
for item in normalized_data_yesterday:
	if 'mrp' in item.keys() and item['mrp'] != None :
		mrp = float(item['mrp'])
		if mrp == 0:
			item['mrp'] = 'NA'
		else:
			item['mrp'] = mrp / max_mrp
	else:
		item['mrp'] = 'NA'

print(normalized_data_yesterday)

for item in normalized_data_today:
	if 'mrp' in item.keys() and item['mrp'] != None :
		mrp = float(item['mrp'])
		if mrp == 0:
			item['mrp'] = 'NA'
		else:
			item['mrp'] = mrp / max_mrp
	else:
		item['mrp'] = 'NA'

print(normalized_data_today)
