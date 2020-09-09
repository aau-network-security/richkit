from richkit.analyse import depth, length, entropy, number_vowels, ratio_vowels, number_consonants, \
    ratio_consonants, number_numerics, ratio_numerics, number_specials, ratio_specials


class FQDN_Features:

    def __init__(self, fqdn_id, fqdn):
        self.fqdn_id = fqdn_id
        self.fqdn = fqdn

    def get_features(self):

        domain_name_features = {
            "fqdn_id": self.fqdn_id,
            "label_number": depth(self.fqdn),
            "lenght": length(self.fqdn),
            "entropy": entropy(self.fqdn),
            "vowels_ratio": ratio_vowels(self.fqdn),
            "vowels_number": number_vowels(self.fqdn),
            "consonants_ratio": ratio_consonants(self.fqdn),
            "consonants_number": number_consonants(self.fqdn),
            "numeric_ratio": ratio_numerics(self.fqdn),
            "numeric_number": number_numerics(self.fqdn),
            "special_ratio": number_specials(self.fqdn),
            "special_number": ratio_specials(self.fqdn),
        }

        return domain_name_features
