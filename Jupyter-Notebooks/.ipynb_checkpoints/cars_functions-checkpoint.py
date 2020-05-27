#========================================================================================================#
# Regressor fit and scorer
#========================================================================================================#




def fit_view_scores(models, X_train, y_train, X_val, y_val):
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




def prediction_plotter(model_name, original_df, X_val, y_val):
    """
    This function takes an instatiated regression model, and test/validation sets.
    It makes a prediction on 10 random rows of the test/validation set and then
    it graphs them with the actual results in a scatter plot.
    
    It is customized to take the argument of the original dataframe I made and show
    the 10 cars it predicted in a table as well ass the visualization of the predictions.
    
    """
    
    # imports
    import numpy as np
    import matplotlib.pyplot as plt
    import random
    import pandas as pd
    import seaborn as sns
    
    
    # Create random sample generator 
    n = random.sample(range(1,1000),1)
    choosen = n[0]
    
   
    # make model predict on val/test
    model_name_pred = model_name.predict(X_val[choosen:choosen+10].round(-3))
    
    # create the predicted price column
    predicted_price = []
    for item in model_name_pred:
        if model_name_pred.shape == (10,1):
            predicted_price.append(item[0].round(2))
        else: predicted_price.append(item.round(2))
     
    # Merge the dataframes so table can show brand and model instead of dummy variables
    cars = pd.merge(y_val.iloc[:][choosen:choosen+10], X_val.iloc[:,:4][choosen:choosen+10], 
                    left_index=True, right_index=True)
    fixed = pd.merge(cars, original_df[['brand','model', 'transmission', 'body_style']], 
                     left_index=True, right_index=True)
    fixed['Predicted Price(£)'] = predicted_price
    
    

    # Order I want the table to be displayed in
    order = ["price(£)", "Predicted Price(£)", "mileage(mi)", "door_count", "engine_size(cc)", "year", "brand", "model","transmission", "body_style"]
    
    
    # add commas to numbers for readability purposes
    fixed['price(£)'] = fixed.apply(lambda x: "{:,}".format(x['price(£)']), axis=1)
    fixed['mileage(mi)']= fixed.apply(lambda x: "{:,}".format(x['mileage(mi)']), axis=1)
    fixed['engine_size(cc)']= fixed.apply(lambda x: "{:,}".format(x['engine_size(cc)']), axis=1)
    fixed['Predicted Price(£)']= fixed.apply(lambda x: "{:,}".format(x['Predicted Price(£)']), axis=1)



    
    # plot results
    fig, ax = plt.subplots(figsize=(8,5))
    ax.scatter(np.arange(10), model_name_pred, label='predicted')
    ax.scatter(np.arange(10), y_val[choosen:choosen+10], label='actual')
    ax.legend()
    ax.set_title('{} Validation Actual vs Predicted for 10 cars'.format(model_name.__class__.__name__))
    ax.set_ylabel('Price (£)')
    ax.set_xticks([])
    
    # Save the plot into my figures folder
    plt.savefig('../figures/prediction_plotter/{}_predicted_output.png'.format(model_name.__class__.__name__))
    
    
    
    return fixed[order].reset_index(drop=True)




#========================================================================================================#
# Correlation heatmap for features
#========================================================================================================#




def heat_map(df, fig_size):
    
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




def view_scores(models, X_train, y_train, X_val, y_val):
    """
    This function takes a list of regressors makes predictions on the validation/test set.
    It then makes a data frame of the results and assigns a heatmap of highest scores(in dark red),
    and lowest scores in light red.
    """
    # imports
    import seaborn as sns
    import pandas as pd
    import sklearn.metrics as sm
    
    # table features
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
        
        # use class object name for method
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
# Grid Search visualizer
#========================================================================================================#




def grid_optimizer(opt_model):
    """
    This function takes a fitted gridsearch model and displays it's results as a seaborn heatmap
    
    """
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    
    opt = pd.DataFrame(opt_model.cv_results_)
    cols = [
        col
        for col in opt.columns
        if ("mean" in col or "std" in col) and "time" not in col
    ]
    params = pd.DataFrame(list(opt.params))
    opt = pd.concat([params, opt[cols]], axis=1, sort=False)

    plt.figure(figsize=[15, 4])
    plt.subplot(121)
    sns.heatmap(
        pd.pivot_table(
            opt,
            index="max_depth",
            columns="min_samples_leaf",
            values="mean_train_score",
        )
        * 100
    )
    plt.title("R2 - Training")
    plt.subplot(122)
    sns.heatmap(
        pd.pivot_table(
            opt, index="max_depth", columns="min_samples_leaf", values="mean_test_score"
        )
        * 100
    )
    plt.title("R2 - Validation")
    
    
    
    
#========================================================================================================#
# 
#========================================================================================================#