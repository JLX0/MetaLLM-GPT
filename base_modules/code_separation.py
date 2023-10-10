import re


class code_control:

    def __init__(self,combined_raw_code,separation_depth=0):
        self.combined_raw_code = combined_raw_code
        self.initial_code_block_list = []
        self.recursively_separated_code_block_list = []
        self.separation_depth = separation_depth
        self.combined_processed_code = ""


    # This function is created using (a previous version of) MetaLLM-GPT.
    @staticmethod
    def concatenate_by_length(str_list, minimum_length, maximum_length, connector="\n\n", idx=0):
        if idx >= len(str_list) - 1:
            return str_list

        if len(str_list[idx]) < minimum_length:
            if idx == 0 or len(str_list[idx - 1]) >= len(str_list[idx + 1]) and len(str_list[idx + 1]) < maximum_length:
                str_list[idx] += connector + str_list.pop(idx + 1)
            elif idx > 0 and len(str_list[idx - 1]) < maximum_length:
                str_list[idx - 1] += connector + str_list.pop(idx)
                idx -= 1

        return code_control.concatenate_by_length(str_list, minimum_length, maximum_length, connector, idx + 1)


    # This function is created using (a previous version of) MetaLLM-GPT.
    @staticmethod
    def concatenate_by_space(str_list, connector="\n\n"):
        i = 1
        while i < len(str_list):
            if str_list[i].startswith(" "):
                str_list[i - 1] += connector + str_list[i]
                str_list.pop(i)
                i -= 1
            i += 1
        return str_list


    # This function is created using (a previous version of) MetaLLM-GPT.
    def separate_into_blocks(self, substring_b="\n", substring_c=" ", minimum_length=100, maximum_length=300):

        # Create a regex pattern to match the markers.
        pattern = re.compile('({0}+{1}*{0}+)+'.format(re.escape(substring_b), re.escape(substring_c)))

        # Find all markers in the string.
        markers = pattern.findall(self.combined_raw_code)

        # Replace markers with a unique separator not present in the string.
        separator = '____SEPARATOR____'
        while separator in self.combined_raw_code:
            separator += '_'

        for marker in markers:
            combined_raw_code = self.combined_raw_code.replace(marker, separator)

        # Split the string using the separator.
        splited_list = self.combined_raw_code.split(separator)

        # Concatenate the strings that start with a space to the previous string.
        self.initial_code_block_list = code_control.concatenate_by_space(splited_list)
        # Concatenate any string that is too short to its shorter adjacent strings, if the shorter adjacent strings is not
        # too long.
        if minimum_length is not None:05555555555555555555555555555555555555555555555555555555555555555555555555555
            self.initial_code_block_list = code_control.concatenate_by_length(self.initial_code_block_list, minimum_length, maximum_length)

    @staticmethod
    def recursive_separation_base(string_a, substring_b="\n", substring_c=" ", substring_d="def", substring_e="class"):

        marker = r'({0}+{1}*{0}+{1}*({2}|{3}))+'.format(re.escape(substring_b), re.escape(substring_c), re.escape(substring_d), re.escape(substring_e))
        separated_strings = re.split(marker, string_a)
        result = [string for string in separated_strings if not re.match(marker, string)]

        code_block_list = []
        skip=False
        for i in range(len(result) - 1):
            if not skip:
              skip=False
              if result[i] == substring_d:
                  code_block_list.append(result[i] + " "+ result[i + 1])
                  skip=True
              else:
                  code_block_list.append(result[i])
            else:
              skip=False

        return code_block_list

    def recursive_separation(self):
        for n in self.initial_code_block_list:
            if n.startswith("def") or n.startswith("class"):
                separated_n_list=code_control.recursive_separation_base(n)

        self.recursively_separated_code_block_list = []

    def separate(self):
        self.separate_into_blocks()
        if self.separation_depth==0:
            return self.initial_code_block_list
        else:
            self.recursive_separation()
            return self.recursively_separated_code_block_list

    def combine(self,processed_code_block_list):
        self.combined_processed_code = ""
        return self.combined_processed_code

        # indentation for recursively separated code blocks

# {"identifier":["path","lines","name","input and output info", "docstring", "content", "indentation", "object_type"]}
# or use a class?
class code_block():
    def __int__(self,identifier,path,lines,name,input_output_info,docstring,content,indentation,object_type):
        self.identifier=identifier
        self.path=path
        self.lines=lines
        self.name=name
        self.input_output_info=input_output_info
        self.docstring=docstring
        self.content=content
        self.indentation=indentation
        self.object_type=object_type #(ordinary code, class or function)

# reorganize?