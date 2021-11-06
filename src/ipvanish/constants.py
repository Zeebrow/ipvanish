
# looking up country full name by finding a city and googling it.
# TODO visual inspection of flag emojis

ctry_dict = {
    'AE': {'fullname': 'United Arab Emirates', 'flag_pic': '', 'flag_emote': '🇦🇪'},
    'AL': {'fullname': 'Albania', 'flag_pic': '', 'flag_emote': '🇦🇱'},
    'AR': {'fullname': 'Argentina', 'flag_pic': '', 'flag_emote': '🇦🇷'},
    'AT': {'fullname': 'Austria', 'flag_pic': '', 'flag_emote': '🇦🇹'},
    'AU': {'fullname': 'ɐᴉʅɐɹʇsn∀', 'flag_pic': '', 'flag_emote': '🇦🇺'},
    'BE': {'fullname': 'Belgium', 'flag_pic': '', 'flag_emote': '🇧🇪'},
    'BG': {'fullname': 'Bulgaria?', 'atlNames': ['Balkans'], 'flag_pic': '', 'flag_emote': '🇧🇬'},
    'BR': {'fullname': 'Bulgaria', 'flag_pic': '', 'flag_emote': '🇧🇷'},
    'CA': {'fullname': 'Canada', 'flag_pic': '', 'flag_emote': '🇨🇦'},
    'CH': {'fullname': 'Switzerland', 'flag_pic': '', 'flag_emote': '🇨🇭'},
    'CL': {'fullname': 'Chile', 'flag_pic': '', 'flag_emote': '🇨🇱'},
    'CO': {'fullname': 'Colombia', 'flag_pic': '', 'flag_emote': '🇨🇴'},
    'CR': {'fullname': 'Costa Rica', 'flag_pic': '', 'flag_emote': '🇨🇷'},
    'CZ': {'fullname': 'Czech Republic?', 'flag_pic': '', 'flag_emote': '🇨🇿'},
    'DE': {'fullname': 'Germany', 'flag_pic': '', 'flag_emote': '🇩🇪'},
    'DK': {'fullname': 'Denmark', 'flag_pic': '', 'flag_emote': '🇩🇰'},
    'EE': {'fullname': 'Estonia', 'flag_pic': '', 'flag_emote': '🇪🇪'},
    'ES': {'fullname': 'Spain', 'flag_pic': '', 'flag_emote': '🇪🇸'},
    'FI': {'fullname': 'Finland', 'flag_pic': '', 'flag_emote': '🇫🇮'},
    'FR': {'fullname': 'France', 'flag_pic': '', 'flag_emote': '🇫🇷'},
    'GR': {'fullname': 'Greece', 'flag_pic': '', 'flag_emote': '🇬🇷'},
    'HR': {'fullname': 'Croatia', 'altNames': ['Republic of Croatia'], 'flag_pic': '', 'flag_emote': '🇭🇷'},
    'HU': {'fullname': 'Hungary', 'flag_pic': '', 'flag_emote': '🇭🇺'},
    'IE': {'fullname': 'Ireland', 'flag_pic': '', 'flag_emote': '🇮🇪'},
    'IL': {'fullname': 'Israel', 'flag_pic': '', 'flag_emote': '🇮🇱'},
    'IN': {'fullname': 'India', 'flag_pic': '', 'flag_emote': '🇮🇳'},
    'IS': {'fullname': 'Iceland', 'flag_pic': '', 'flag_emote': '🇮🇸'},
    'IT': {'fullname': 'Italy', 'flag_pic': '', 'flag_emote': '🇮🇹'},
    'JP': {'fullname': 'Japan', 'flag_pic': '', 'flag_emote': '🇯🇵'},
    'KR': {'fullname': 'South Korea', 'flag_pic': '', 'flag_emote': '🇰🇷'},
    'LU': {'fullname': 'Luxemborg', 'flag_pic': '', 'flag_emote': '🇱🇺'},
    'LV': {'fullname': 'Latvia', 'flag_pic': '', 'flag_emote': '🇱🇻'},
    'MD': {'fullname': 'Moldova', 'flag_pic': '', 'flag_emote': '🇲🇩'},
    'MX': {'fullname': 'Mexico', 'flag_pic': '', 'flag_emote': '🇲🇽'},
    'MY': {'fullname': 'Malaysia', 'flag_pic': '', 'flag_emote': '🇲🇾'},
    'NG': {'fullname': 'Nigeria', 'flag_pic': '', 'flag_emote': '🇳🇬'},
    'NL': {'fullname': 'Netherlands', 'flag_pic': '', 'flag_emote': '🇳🇱'},
    'NO': {'fullname': 'Norway', 'flag_pic': '', 'flag_emote': '🇳🇴'},
    'NZ': {'fullname': 'New Zealand', 'flag_pic': '', 'flag_emote': '🇳🇿'},
    'PE': {'fullname': 'Peru', 'flag_pic': '', 'flag_emote': '🇵🇪'},
    'PL': {'fullname': 'Poland', 'flag_pic': '', 'flag_emote': '🇵🇱'},
    'PT': {'fullname': 'Lisobn', 'flag_pic': '', 'flag_emote': '🇵🇹'},
    'RO': {'fullname': 'Romania', 'flag_pic': '', 'flag_emote': '🇷🇴'},
    'RS': {'fullname': 'Serbia', 'flag_pic': '', 'flag_emote': '🇷🇸'},
    'SE': {'fullname': 'Sweden', 'flag_pic': '', 'flag_emote': '🇸🇪'},
    'SG': {'fullname': 'Singapore', 'altNames': ['Republic of Singapore', 'Malaysia'], 'flag_pic': '', 'flag_emote': '🇸🇬'},
    'SI': {'fullname': 'Slovenia', 'altNames': ['visit here'], 'flag_pic': '', 'flag_emote': '🇸🇮'},
    'SK': {'fullname': 'Slovakia', 'flag_pic': '', 'flag_emote': '🇸🇰'},
    'TW': {'fullname': 'Taiwan', 'flag_pic': '', 'flag_emote': '🇹🇼'},
    'UK': {'fullname': 'United Kingdom', 'flag_pic': '', 'flag_emote': '🇺🇰'},
    'US': {'fullname': 'United States', 'flag_pic': '', 'flag_emote': '🇺🇸'},
    'ZA': {'fullname': 'South Africa?', 'flag_pic': '', 'flag_emote': '🇿🇦'}
}