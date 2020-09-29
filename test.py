from urllib import parse

# url = parse.urljoin("https://www.vlerick.com", "/1234")
#
# url2 = parse.urljoin("https://www.vlerick.com", "https://www.vlerick.com/1234")

list1 = [1,2,3,4,5]
list2 = [1,1,1,1,1]

print(list(zip(list1,list2)))