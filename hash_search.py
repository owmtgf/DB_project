import hashlib


def find_substring_indices(main_string, sub_string):
    flag = False
    main_string_length = len(main_string)
    sub_string_length = len(sub_string)
    prime_number = 31
    cut = 10 ** 9 + 9

    prefix_hashes = [0] * (main_string_length + 1)
    powers_of_prime = [1] * (main_string_length + 1)
    for i in range(1, main_string_length + 1):
        prefix_hashes[i] = (prefix_hashes[i - 1] + ord(main_string[i - 1]) * powers_of_prime[i - 1]) % cut
        powers_of_prime[i] = (powers_of_prime[i - 1] * prime_number) % cut
    sub_string_hash = 0
    for i in range(sub_string_length):
        sub_string_hash = (sub_string_hash + ord(sub_string[i]) * powers_of_prime[i]) % cut

    for i in range(sub_string_length - 1, main_string_length):
        current_hash = (prefix_hashes[i + 1] - prefix_hashes[i - sub_string_length + 1]) % cut
        if current_hash == (sub_string_hash * powers_of_prime[i - sub_string_length + 1]) % cut:
            flag = True

    return flag


def find_all_elems(main_string, sub_string):
    sub_string = sub_string.split()
    for i in sub_string:
        try:
            flag = find_substring_indices(main_string, i)
        except:
            flag = False
        if not flag:
            return False
    return True


def encode_password(password):

    md5_hash = hashlib.md5()
    password = password.encode('utf-8')
    md5_hash.update(password)

    return md5_hash.hexdigest()
