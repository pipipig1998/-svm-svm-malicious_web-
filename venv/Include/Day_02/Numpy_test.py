import numpy as np
if __name__ == '__main__':
    narry=np.array([
        [1,2,3],
        [4,5,6]
    ])
    print(narry.shape)
    narry=narry.reshape(3,2)
    print(narry)


    studenttype=np.dtype(
        {
            'names':['name','chinese','math','english'],
            'formats':['S32',np.float,np.float,np.float]
        }
    )
    narry=np.array(
        [
            ('wangshuai',100,100,100),
            ('pipipig',95,98,97),
            ('tuzi',30,30,30)
        ],dtype=studenttype
    )
    print(narry)
    chinese=narry[:]['chinese']
    print(np.mean(chinese))

    a=np.arange(1,8,2)
    b=np.linspace(1,7,4)
    print(a)
    print(b)
    print(np.add(b,a))
    print(np.multiply(b,a))

    print(a.var())
    print(a.std())