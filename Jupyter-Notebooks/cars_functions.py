





#========================================================================================================#
# Regressor fit and scorer
#========================================================================================================#




def FitViewScores(models, X_train, y_train, X_val, y_val):
    """
    This function takes a list of regressors, train and test data sets and fits the
    regressor to the train data set and makes predictions on the validation/test set.
    It then makes a data frame of the results and assigns a heatmap of highest scores(in dark red),
    and lowest scores in light red.
    """
    # imports
    import seaborn as sns
    import pandas as pd
    import sklearn.metrics as sm
    
    # results containers
    
    
    model_name = []
    train_r2 = []
    val_r2 = []
    train_mse = []
    val_mse = []
    train_mae = []
    val_mae = []
    
    for reg in models:
        reg.fit(X_train, y_train)
        
        #predictions
        y_pred = reg.predict(X_train)
        val_pred = reg.predict(X_val)
        
        
        model_name.append(reg.__class__.__name__)
        
        train_r2.append(round(sm.r2_score(y_train, y_pred),2))
        val_r2.append(round(sm.r2_score(y_val, val_pred),2))
        
        train_mse.append(round(sm.mean_squared_error(y_train, y_pred),2))
        val_mse.append(round(sm.mean_squared_error(y_val, val_pred),2))
        
        train_mae.append(round(sm.mean_absolute_error(y_train, y_pred),2))
        val_mae.append(round(sm.mean_absolute_error(y_val, val_pred),2))
        #build df
        data={ 
               'Method': model_name,
               'Train R2': train_r2, 
               'Validation R2': val_r2,
               'Train MSE': train_mse,
               'Validation MSE': val_mse,
               'Train MAE': train_mae,
               'Validation MAE': val_mae}
    
        # stylize
        cm = sns.light_palette("violet", as_cmap=True)
        results = pd.DataFrame(data).sort_values('Validation R2',
                            ascending=False).style.background_gradient(cmap=cm)
    return results



#========================================================================================================#
# Plotting predictions
#========================================================================================================#




def PredictionPlotter(model_name, X_val, y_val):
    """
    This function takes an instatiated regression model, and test/validation sets.
    It makes a prediction on 10 random rows of the test/validation set and then
    it graphs them with the actual results in a scatter plot.
    
    """
    
    # imports
    import numpy as np
    import matplotlib.pyplot as plt
    import random
    
    
    # Create random generator 
    n = random.sample(range(1,1000),1)
    choosen = n[0]
    
   
    # make model predict on val/test
    model_name_pred = model_name.predict(X_val[choosen:choosen+10].round(-3))
    
    # plot results
    fig, ax = plt.subplots(figsize=(8,5))
    ax.scatter(np.arange(10), model_name_pred, label='predicted')
    ax.scatter(np.arange(10), y_val[choosen:choosen+10], label='actual')
    ax.legend()
    ax.set_title('{} Validation Actual vs Predicted for 10 rows'.format(model_name.__class__.__name__))
    ax.set_ylabel('Price (£)')
    ax.set_xticks([])
    plt.savefig('../figures/prediction_plotter/{}_predicted_output.png'.format(model_name.__class__.__name__))
    
    return plt.show()



#========================================================================================================#
# Correlation heatmap for features
#========================================================================================================#



def HeatMap(df, fig_size):
    
    """
    
    This function takes the arguments for a pandas data frame and a tuple for size.
    It uses a custom seaborn color map and applies a mask to hide the repeat correlated features.
    
    """
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    corr = df.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    
    plt.figure(figsize=fig_size)
    sns.heatmap(corr,annot=True, mask=mask, cmap='RdBu_r')
    plt.autoscale()
    plt.savefig('../figures/heatmap.png')
    
    return plt.show()



#========================================================================================================#
# Regressor scorer
#========================================================================================================#




def ViewScores(models, X_train, y_train, X_val, y_val):
    """
    This function takes a list of regressors makes predictions on the validation/test set.
    It then makes a data frame of the results and assigns a heatmap of highest scores(in dark red),
    and lowest scores in light red.
    """
    # imports
    import seaborn as sns
    import pandas as pd
    import sklearn.metrics as sm
    
    # results containers
    
    model_name = []
    train_r2 = []
    val_r2 = []
    train_mse = []
    val_mse = []
    train_mae = []
    val_mae = []
    
    for reg in models:
        #predictions
        y_pred = reg.predict(X_train)
        val_pred = reg.predict(X_val)
        
        
        model_name.append(reg.__class__.__name__)
        
        
        train_r2.append(round(sm.r2_score(y_train, y_pred),2))
        val_r2.append(round(sm.r2_score(y_val, val_pred),2))
        
        train_mse.append(round(sm.mean_squared_error(y_train, y_pred),2))
        val_mse.append(round(sm.mean_squared_error(y_val, val_pred),2))
        
        train_mae.append(round(sm.mean_absolute_error(y_train, y_pred),2))
        val_mae.append(round(sm.mean_absolute_error(y_val, val_pred),2))
        #build df
        data={ 
               
               'Method': model_name,
               'Train R2': train_r2, 
               'Validation R2': val_r2,
               'Train MSE': train_mse,
               'Validation MSE': val_mse,
               'Train MAE': train_mae,
               'Validation MAE': val_mae}
    
        # stylize
        cm = sns.light_palette("violet", as_cmap=True)
        results = pd.DataFrame(data).sort_values('Validation R2',
                            ascending=False).style.background_gradient(cmap=cm)
    return results

