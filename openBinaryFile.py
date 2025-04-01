with open('test.txt', 'rb') as archive:
    file = archive.read()
    
    #retorna o valor em binario
    binaryEncode=' '.join(format(byte,'016b') for byte in file)
    
    #retorna o valor decima de 8bits
    hexadecimaEncode=' '.join(format(type(byte,'016b') for byte in file))
    print(hexadecimaEncode)