#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# 
# For this project, we'll pretend we're working as data analysts for a company that builds Android and iOS mobile apps. We make our apps available on Google Play and the App Store.
# 
# We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means our revenue for any given app is mostly influenced by the number of users who use our app. Our goal for this project is to analyze data to help our developers understand what kinds of apps are likely to attract more users.

# ## 1. Exploring the data sets 

# In[1]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# Open datasets: Applestore and GooglePlayStore and print the column names and try to identify the columns that could help us with our analysis.

# In[2]:


from csv import reader

apple_dataset = list(reader(open('AppleStore.csv')))
google_dataset = list(reader(open('googleplaystore.csv')))


# Printing Apple App Store data set.

# In[3]:


explore_data(apple_dataset, 0, 5)


# Printing Google Play Store data set.

# In[4]:


explore_data(google_dataset, 0, 5)


# Find the number of rows and columns of each data set.

# In[5]:


def count_columns(dataset):
    return len(dataset[0])

def count_rows(dataset, header = False):
    count = 0
    for element in dataset[1:]:
        count +=1
    if header:
        count += 1
    
    return count


# Rows and columns in Apple App Store data set.

# In[6]:


print('Columns: ' + str(count_columns(apple_dataset)))
print('Rows: ' + str(count_rows(apple_dataset)))


# Rows and columns in Google Play Store data set.

# In[7]:


print('Columns: ' + str(count_columns(google_dataset)))
print('Rows: ' + str(count_rows(google_dataset)))


# ## 2. Cleaning some data

# Exploring posible wrong data in row 10473 in Google Play Store data set. 

# In[8]:


print(google_dataset[0])
print('\n')
print(google_dataset[1])
print('\n')
print(google_dataset[10473])


# Deleting row 10473 in Google Play Store data set.

# In[9]:


del google_dataset[10473]


# ### Duplicate data 

# In the last step, we started the data cleaning process and deleted a row with incorrect data from the Google Play data set. If you explore the Google Play data set long enough, or look at the discussions section from the source of the dataset, you'll notice some apps have duplicate entries.

# In[10]:


for app in google_dataset[1:]:
    if app[0] == 'Instagram':
        print(app)


# In total, there are 1,181 cases where an app occurs more than once.

# In[11]:


duplicate_apps = []
unique_apps = []

for app in google_dataset[1:]:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
print(len(duplicate_apps))


# We don't want to count certain apps more than once when we analyze data, so we need to remove the duplicate entries and keep only one entry per app. One thing we could do is remove the duplicate rows randomly, but we could probably find a better way.
# 
# If you examine the rows we printed above for the Instagram app, the main difference happens on the fourth position of each row, which corresponds to the number of reviews. The different numbers show that the data was collected at different times.
# 
# We could use this information to build a criterion for removing the duplicates. The higher the number of reviews, the more recent the data should be. Rather than removing duplicates randomly, we'll only keep the row with the highest number of reviews and remove the other entries for any given app.

# In[12]:


reviews_max = {}
for app in google_dataset[1:]:
    name = app[0]
    reviews = float(app[3])
    
    if name not in reviews_max:
        reviews_max[name] = reviews
    elif reviews_max[name] < reviews:
        reviews_max[name] = reviews

android_clean = []
already_added = []
for app in google_dataset[1:]:
    name = app[0]
    reviews = float(app[3])
    if reviews_max[name] == reviews and name not in already_added:
        android_clean.append(app)
        already_added.append(name)
        
print('Dictionary: ' + str(len(reviews_max)))
print('Clean List: ' + str(len(android_clean)))


# ### Only English Apps 

# In the previous step, we managed to remove the duplicate app entries in the Google Play data set. The language we use for our apps is English, and we'd like to analyze only the apps that are directed toward an English-speaking audience. However, if we exploring the data long enough, we'll find that both data sets have apps whose name suggests that they are not direct toward an English-speaking audience.

# In[13]:


print(apple_dataset[814][1])
print(apple_dataset[6732][1])
print('\n')
print(android_clean[4412][0])
print(android_clean[7940][0])


# We're not interested in keeping these kind of apps, so we'll remove them. One way to go about this is to remove each app whose name contains a symbol that is not commonly used in English text — English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks (., !, ?, ;, etc.), and other symbols (+, *, /, etc.).
# 
# The numbers corresponding to the characters we commonly use in an English text are all in the range 0 to 127, according to the ASCII (American Standard Code for Information Interchange) system. Based on this number range, we can build a function that detects whether a character belongs to the set of common English characters or not. If the number is equal to or less than 127, then the character belongs to the set of common English characters, otherwise it doesn't.
# 
# The emojis and some characters like ™ fall outside the ASCII range and have corresponding numbers that are over 127. f we're going to use the function we've created, we'll lose useful data since many English apps will be incorrectly labeled as non-English. To minimize the impact of data loss, we'll only remove an app if its name has more than three characters with corresponding numbers falling outside the ASCII range. This means all English apps with up to three emoji or other special characters will still be labeled as English. Our filter function is still not perfect, but it should be fairly effective.

# In[14]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# Removing non-English apps from both data sets.

# In[15]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in apple_dataset:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
print('Android: ' + str(len(android_english)))
print('iOS: ' + str(len(ios_english)))


# ## 3. Isolating Free Apps 

# As we mentioned in the introduction, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. Our data sets contain both free and non-free apps, and we'll need to isolate only the free apps for our analysis.

# In[16]:


android_free_apps = []
ios_free_apps = []

for app in android_english:
    if app[7] == '0':
        android_free_apps.append(app)

for app in ios_english:
    if app[4] == '0.0':
        ios_free_apps.append(app)
        
print('Android free apps: ' + str(len(android_free_apps)))
print('iOS free apps: ' + str(len(ios_free_apps)))


# So far, we spent a good amount of time on cleaning data, and:
# 
# - Removed inaccurate data
# - Removed duplicate app entries
# - Removed non-English apps
# - Isolated the free apps
# 
# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# - Build a minimal Android version of the app, and add it to Google Play.
# - If the app has a good response from users, we then develop it further.
# - If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both the App Store and Google Play, we need to find app profiles that are successful on both markets. For instance, a profile that might work well for both markets might be a productivity app that makes use of gamification.

# In[17]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        


# In[18]:


display_table(ios_free_apps, -5)


# We can see that among the free English apps, more than a half (58.16%) are games. Entertainment apps are close to 8%, followed by photo and video apps, which are close to 5%. Only 3.66% of the apps are designed for education, followed by social networking apps which amount for 3.29% of the apps in our data set.
# 
# The general impression is that App Store (at least the part containing free English apps) is dominated by apps that are designed for fun (games, entertainment, photo and video, social networking, sports, music, etc.), while apps with practical purposes (education, shopping, utilities, productivity, lifestyle, etc.) are more rare. However, the fact that fun apps are the most numerous doesn't also imply that they also have the greatest number of users — the demand might not be the same as the offer.
# 
# Let's continue by examining the Genres and Category columns of the Google Play data set (two columns which seem to be related).

# In[19]:


display_table(android_free_apps, 1)


# The landscape seems significantly different on Google Play: there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.
# 
# Even so, practical apps seem to have a better representation on Google Play compared to App Store. This picture is also confirmed by the frequency table we see for the Genres column:

# In[20]:


display_table(android_free_apps, -4)


# The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular (it has more categories). We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.

# # Most Popular Apps by Genre on the App Store
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but for the App Store data set this information is missing. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# Below, we calculate the average number of user ratings per app genre on the App Store:

# In[21]:


freq_table_prime_genre = freq_table(ios_free_apps, -5)
for genre in freq_table_prime_genre:
    total = 0
    len_genre = 0
    for app in ios_free_apps:
        genre_app = app[-5]
        if(genre_app == genre):
            total += float(app[5])
            len_genre += 1
    result = total / len_genre
    print(genre,':', result)


# On average, navigation apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together:

# In[22]:


for app in ios_free_apps:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5])


# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. 
# 
# Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating

# In[23]:


for app in ios_free_apps:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us:
# 
# Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.
# 
# Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.
# 
# Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.
# 
# Now let's analyze the Google Play market a bit.

# # Most Popular Apps by Genre on Google Play
# For the Google Play market, we actually have data about the number of installs, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.)
# 
# Display installs column:

# In[24]:


display_table(android_free_apps, 5)


# One problem with this data is that is not precise. For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to get an idea which app genres attract the most users, and we don't need perfect precision with respect to the number of users.
# 
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on.
# 
# To perform computations, however, we'll need to convert each install number to float — this means that we need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error. We'll do this directly in the loop below, where we also compute the average number of installs for each genre (category).

# In[25]:


categories_android = freq_table(android_free_apps, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_free_apps:
        category_app = app[1]
        if category == category_app:
            install = app[5]
            install = install.replace('+', '')
            install = install.replace(',', '')
            total += float(install)
            len_category += 1
    avg_install = total / len_category
    print(category, ':', avg_install)


# On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

# In[27]:


for app in android_free_apps:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times:

# In[29]:


under_100_m = []

for app in android_free_apps:
    installs = app[5]
    installs = installs.replace('+', '')
    installs = installs.replace(',', '')
    n_installs = float(installs)
    if app[1] == 'COMMUNICATION' and n_installs < 100000000:
        under_100_m.append(n_installs)
        
sum(under_100_m) / len(under_100_m)


# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[31]:


for app in android_free_apps:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps that skew the average:

# In[32]:


for app in android_free_apps:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[33]:


for app in android_free_apps:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# # Conclusions
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
