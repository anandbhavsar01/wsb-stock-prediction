def get_words(post):
    split_l = post.split(" ")
    tmp_list = ' '.join(split_l).split()
    normd = [ww.lower() for ww in tmp_list]
    return normd

def remove_links(post):
    url_pattern = re.compile(r'https?//\S+|www\.\S+')
    return url_pattern.sub(r'', post)
    
def remove_bad_chars(post):
    other_chars = ['*', '[', ']', '; ',":","“","“","”","-","=","|","^"] 
    for char in other_chars:
        post = post.replace(char, '')
    return post

def get_processed_data(data):
    data=data.reset_index()
    
    # remove bad characters
    data["title"]=data["title"].apply(remove_bad_chars)
    
    # remove all links present in a post title
    data["title"]=data["title"].apply(remove_links)
    
    # put posts into list of words
    data["title"]=data["title"].apply(get_words)
    return data

def convert_to_dict(data,col):
    my_dict = {}
    for index, row in data.iterrows():
        my_dict[index] = row[col]
    return my_dict