import httpx
def main():
    resp = httpx.get("https://news.ycombinator.com/jobs",timeout = 10)
    s = ''
    org = resp.content.decode('utf-8')
    print(org)
    for char in org:
        if s.startswith('<') and s.endswith('>'):
            print(s)
            s = ''
        else:
            s += char

if __name__ == "__main__":
    main()
