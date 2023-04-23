from bitarray import bitarray
from ByteAnalyze import ByteAnalyze


class HaffmanCoder:
    def __init__(self, SortedOketsX=None, message=None, alph_chars=None):
        if type(SortedOketsX) != type({}) and SortedOketsX != None:
            raise "please, check arg. Message is not SortedOketsX"
        if alph_chars != None and SortedOketsX != None:
            raise ("No sence: SortedOketsX included alph_chars")
        if alph_chars != None:
            try:
                if type("str") == type(message):
                    endcoded_message = message.encode("utf8")
                elif type(bytearray(bytes([1]))) == type(message):
                    endcoded_message = bytes(message)
                else:
                    endcoded_message = message
                ba = ByteAnalyze(endcoded_message, alph_chars)
                ba.Alph_in_X()
                SortedOketsX = ba.ReturnOketsInFile()
            except NameError:
                raise ("module ByteAnalyze not be included")
        if SortedOketsX != None and message != None:
            self.sorted_okets = self.Haffman_Sort(SortedOketsX)
            self.huff_dict = self.Haffed()
            self.byte_coded_message = self.CodeThisToBytearray(endcoded_message)
            self.byte_uncoded_message = self.DecodeThisToStr(self.byte_coded_message)
        if SortedOketsX != None and message == None:
            self.sorted_okets = self.Haffman_Sort(SortedOketsX)
            self.huff_dict = self.Haffed()
            self.byte_coded_message = None
            self.byte_uncoded_message = None
        if SortedOketsX == None and message == None and alph_chars == None:
            self.sorted_okets = None
            self.huff_dict = None
            self.byte_coded_message = None
            self.byte_uncoded_message = None

    def Haffman_Sort(self, SortedOketsX):
        sorted_by_haff = dict(sorted(
            (dict(sorted(SortedOketsX.items(),
                         key=lambda x: x[0], reverse=False))).items(),
            key=lambda x: x[1], reverse=False))
        return sorted_by_haff

    def Haffed(self, sorted_okets=None):
        if sorted_okets == None:
            if self.sorted_okets == None:
                raise Exception('None on None. Try put sorted SortedOkets on init, or put okets here')
            else:
                sorted_okets = self.sorted_okets
        else:
            self.sorted_okets = sorted_okets

        X = dict(sorted_okets)
        returned = X.copy()
        for key, value in returned.items():
            returned[key] = bytearray()
        while (len(X) != 1):
            X_keys = list(X.keys()).copy()
            X[X_keys[0] + "-_-" + X_keys[1]] = X[X_keys[0]] + X[X_keys[1]]
            for keyelem in str(X_keys[0]).split("-_-"):
                returned[keyelem].insert(0, 1)
            for keyelem in str(X_keys[1]).split("-_-"):
                returned[keyelem].insert(0, 0)
            X.pop(X_keys[0])
            X.pop(X_keys[1])
            X = dict(sorted(
                (dict(sorted(X.items(),
                             key=lambda x: x[0], reverse=False))).items(),
                key=lambda x: x[1], reverse=False))
        #    returned_str = bytes()
        #    for key, value in returned.items():
        #        returned_str = returned_str + bytes(returned[key])
        return returned

    def CodeThisToBytearray(self, message, haff_dict=None, sorted_okets=None):
        if sorted_okets != None:
            self.sorted_okets = sorted_okets
            self.huff_dict = self.Haffed(sorted_okets)
        else:
            if haff_dict == None:
                if self.huff_dict == None:
                    raise Exception('None on None. Try put haff_dict on init, or put haff_dict here')
                haff_dict = self.huff_dict
            returned = bitarray()
            for elem in message:
                if int == type(elem):
                    elem = str(bytes([elem]))
                #          print(elem, type(elem), int, 24, int == type(elem))
                #          bytese = bytearray(haff_dict[elem])
                #      for by in bytese:
                #           a = bytearray(by)
                #         returned.extend(a)
                #           else:
                for by in haff_dict[elem]:
                    returned.append(by)
            #          print(by)
            #        x = bitarray()
            #        x.frombytes(by)
            #         print(x)
            returned = returned.tobytes()
            self.byte_coded_message = returned
            return returned

    def DecodeThisToStr(self, byte_coded_message=None, haff_dict=None):
        if byte_coded_message == None:
            if self.byte_coded_message == None:
                raise Exception(
                    'None on None. Try put byte_coded_message on init, or put byte_coded_message dict or okets here')
            byte_coded_message = self.byte_coded_message
        if haff_dict == None:
            if self.huff_dict == None:
                raise Exception('None on None. Try put sorted SortedOkets on init, or put encoded dict or okets here')
            haff_dict = self.huff_dict
        x = bitarray()
        x.frombytes(byte_coded_message)
        byte_coded_message = bytearray()
        for elem in x:
            byte_coded_message.append(elem)
        returned = ""
        haff_valuse = list(haff_dict.values())
        haff_key = list(haff_dict.keys())
        bytes_list_in_haff_dict = [bytes(val) for val in haff_valuse]
        ba = ByteAnalyze(bytes(byte_coded_message), bytes_list_in_haff_dict)
        for elem in ba.EnFile:
            if elem in bytes_list_in_haff_dict:
                returned = returned + str(haff_key[haff_valuse.index(bytearray(elem))])[2:-1]
        self.byte_uncoded_message = returned
        return returned
