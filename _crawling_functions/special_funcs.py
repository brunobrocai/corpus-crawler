def make_absolute_links(links, base_url):
    absolutes = {
        base_url + link if link.startswith('/') else link for link in links
    }
    absolutes = {
        base_url + '/phpbb' + link[1:] if link.startswith('./')
        else link for link in absolutes
    }
    absolutes = {
        base_url + link
        if not link.startswith('https')
        else link for link in absolutes
    }
    return absolutes
