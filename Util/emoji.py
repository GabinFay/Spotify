def get_surrogates(long_code):
    h = int(np.floor((long_code - 0x10000) / 0x400) + 0xD800)
    l = int((long_code - 0x10000) % 0x400 + 0xDC00)
    return ''.join(map(chr, [h,l]))

def emoji_from_surrogates(surrogate_codes):
    return surrogate_codes.encode('utf-16',  'surrogatepass').decode('utf-16')

def emoji_from_long_code(long_code):
    return self.emoji_from_surrogates(self.get_surrogates(long_code))

fish = emoji_from_surrogates('\ud83d\udc1f')
blood_drop = emoji_from_long_code(0x1FA78)
