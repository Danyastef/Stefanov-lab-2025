def fun(s):
    if '@' not in s or '.' not in s or not s.strip():
        return False
    username, domain = s.split('@', 1)
    if '.' not in domain:
        return False
    websitename, extension = domain.rsplit('.', 1)
    if not (username.replace('-', '').replace('_', '').isalnum()) or not (username.replace('-', '').replace('_', '').isascii()):
        return False
    if not websitename.isascii() or not websitename.isalnum():
        return False
    if not extension.isalpha() or len(extension) > 3 or not extension.isascii():
        return False
    return True

def filter_mail(emails):
    return list(filter(fun, emails))

if __name__ == '__main__':
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())

    filtered_emails = filter_mail(emails)
    filtered_emails.sort()
    print(filtered_emails)