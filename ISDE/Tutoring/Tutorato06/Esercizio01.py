from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def compress_file(self, filename : str) -> str:
        pass

class CompressZip(Strategy):

    def compress_file(self, filename : str) -> str:
        return filename + '.zip'

class CompressRar(Strategy):

    def compress_file(self, filename : str) -> str:
        return filename + '.rar'


class Compressor:
    def __init__(self, file_input : str, strategy : Strategy) -> None:
        self.file_input = file_input
        self.strategy = strategy

    def compress_file(self) -> None:
        print(f"file has been compressed! {self.strategy.compress_file(self.file_input)}")


if __name__ == "__main__":
    files = ["voti","database"]
    for file in files:
        zip_compressor  = Compressor(file, CompressZip())
        rar_compressor = Compressor(file, CompressRar())
        zip_compressor.compress_file()
        rar_compressor.compress_file()