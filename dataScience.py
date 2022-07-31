import mathematicalFunctions as mf

class SimpleLinearRegression:    
    def __init__(self):
        self.b0 = None
        self.b1 = None
        self.tss_val = None
        self.ess_val = None
        self.rss_val = None
        self.R_square = None
        
    
    def fit(self,x,y):
        x_mean = mf.mean(x)
        y_mean = mf.mean(y)
        self.__b1_parameter(x,y,x_mean,y_mean)
        self.__b0_parameter(x_mean,y_mean)
        y_predicts = self.__leastsquares_predict(x)
        self.__tss_ess_rss_rsquare(y,y_mean,y_predicts)
        
        
    def __b0_parameter(self,x_mean,y_mean):
        self.b0 = y_mean - self.b1*x_mean
        
    
    def __b1_parameter(self,x,y,x_mean,y_mean):
        value0 = 0
        value1 = 0   
        for j in range(len(x)):
            value0 = value0 + (y[j] - y_mean)*(x[j] - x_mean)
            value1 = value1 + (x[j] - x_mean)**2
            
        self.b1 = value0/value1 
    
    
    def __leastsquares_predict(self,x):
        y_predicts = []
        for i in range(len(x)):
            y_predicts.append(self.b0 + self.b1*x[i])
        return y_predicts
    
    
    def __tss_ess_rss_rsquare(self,y,y_mean,y_predicts):
        self.tss_val = 0
        self.ess_val = 0
        self.rss_val = 0
        for i in range(len(y)):
            print("Step:",i)
            self.tss_val = self.tss_val + (y[i]-y_mean)**2
            self.ess_val = self.ess_val + (y_predicts[i]-y_mean)**2
            self.rss_val = self.rss_val + (y[i]-y_predicts[i])**2
        print("Finished fit!") 
        self.R_square = self.ess_val/self.tss_val
        
        
    def predict(self,x):
        total = self.b0+self.b1*x
        
        return total
        
     
    
class MultiLinearRegression:   
    def __init__(self):
        self.weights = []
        self.tss_val = None
        self.ess_val = None
        self.rss_val = None
        self.R_square = None
        
        
    def fit(self,x,y):  
        X,Y,row,column = self.__data_convert(x,y)
        XX_transpose,YX_transpose = self.__matrix_multiplication(X,Y,row,column)
        unit_matrix = self.__matrix_inverse(XX_transpose,YX_transpose)
        self.__calculate_parameter(unit_matrix,YX_transpose, row, column)
        y_predicts = self.__real_value_predict(X, row)
        self.__tss_ess_rss_rsquare(Y, y_predicts, row)
        print("Finished fit!")
        

    def __data_convert(self,x,y):  
        X = []
        Y = []
        ones = []
        
        if(type(x)!=list):         
            for i in y.columns:
               Y = y[i].tolist()
                         
            for i in x.columns:
                X.append(x[i].tolist())             
            row = len(Y)
            column = len(X)
               
        elif(type(x)==list):         
            column = len(x)
            row = len(y)
            Y = y
            X = x

        for i in range(row):
            ones.append(1)
        
        X.insert(0,ones)

        return X,Y,row,column
    
    
    def __matrix_multiplication(self,X,Y,row,column):
        XX_transpose = []
        for m in range(column+1):
            add_list = []
            for i in range(column+1):
                total = 0           
                for j in range(row):
                    total += X[m][j]*X[i][j]
    
                add_list.append(total)
            XX_transpose.append(add_list)
      
        YX_transpose = []
        for i in range(column+1):
            add_list = []
            total = 0 
            for j in range(row):
                total += X[i][j]*Y[j]
                
            YX_transpose.append(total)
        
        return XX_transpose,YX_transpose
    
    
    def __matrix_inverse(self,XX_transpose,YX_transpose): 
        matrix_shape = len(XX_transpose)
        unit_matrix = mf.identitymatrix(matrix_shape)
        
        for i in range(matrix_shape):
            d = XX_transpose[i][i]       
            for j in range(matrix_shape):
                XX_transpose[i][j] = XX_transpose[i][j]/d
                unit_matrix[i][j] = unit_matrix[i][j]/d
            for x in range(matrix_shape):
                if(x!=i):
                    k = XX_transpose[x][i]
                    for j in range(matrix_shape):
                        XX_transpose[x][j] = XX_transpose[x][j]-(XX_transpose[i][j]*k)
                        unit_matrix[x][j] = unit_matrix[x][j]-(unit_matrix[i][j]*k)
    
        return unit_matrix
    
    
    def __calculate_parameter(self,unit_matrix,YX_transpose,row,column):
        for i in range(column+1):
            total = 0 
            for j in range(column+1):
                total += unit_matrix[i][j]*YX_transpose[j]
            self.weights.append(total)
            
            
    def __real_value_predict(self,data_x,row):
        y_predicts = []
        for j in range(row):
            total = 0
            for i in range(len(self.weights)-1):
                total += data_x[i+1][j]*self.weights[i+1]
                
            total += self.weights[0]
            
            y_predicts.append(total)
        
        return y_predicts
            
    
    def __tss_ess_rss_rsquare(self,Y,y_predicts,row):
        self.tss_val = 0
        self.ess_val = 0
        self.rss_val = 0
        y_mean = mf.mean(Y)
        for i in range(row):
            self.tss_val = self.tss_val + (Y[i]-y_mean)**2
            self.ess_val = self.ess_val + (y_predicts[i]-y_mean)**2
            self.rss_val = self.rss_val + (Y[i]-y_predicts[i])**2
         
        self.R_square = 1-(self.rss_val/(row-len(self.weights)))/(self.tss_val/(row-1))
            
            
    def predict(self,data_x):
        total = 0
        for i in range(len(self.weights)-1):
            total += data_x[i]*self.weights[i+1]
        total += self.weights[0]

        return total