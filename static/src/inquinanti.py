import json


import pandas as pd


class Inquinante(object):

    def __init__(self, name, limit, method):
        """
            name: name of air pollutter
            limit: value of pollutter's threshold
            method: 'daily', 'hourly', 'yearly'
        """
        
        with open('static/data/default_info/agenti_e_centraline.json') as f:
            agenti_centraline = json.load(f)
            self.list_inquinanti = agenti_centraline['inquinanti']
            self.list_centraline = agenti_centraline['centraline']
        
        self.name = name
        self.limit = limit
        self.method = method
        
    def pollutant_dataframe(self, df):
        """Returns the df wrt to the pollutant of interest.
        
            df: dataframe to make computations on
        """
        
        try:
            assert self.name in self.list_inquinanti
            return df[df['inquinante'] == self.name]
        except AssertionError:
            print ('The pollutant doesn\'t exist')
        
    def average(self, df, anno):
        """Returns the average df wrt the year of interest.
        
            df: dataframe to make computations on
            anno: year of interest
        """
        
        try:
            assert self.name in self.list_inquinanti
            
            if self.method == 'hourly':
                return self._hourly_avg(df, anno)
        
            elif self.method == 'daily':
                return self._daily_avg(df, anno)
            
            elif self.method == 'yearly':
                return self._yearly_avg(df, anno)
            
            else: 
                print ('You select an invalid method!')
        
        except AssertionError:
            print ('The inserted inquinante is not in the list of possible inquinanti')
        
        
    def _hourly_avg(self, df, anno):
        """Returns the hourly average df wrt the year of interest.
        
            df: dataframe to make computations on
            anno: year of interest
        """
        
        # Compute the mean over the df referring to the pullutter
        df_media = self.pollutant_dataframe(df).groupby('data_ora_time').max().ix[-1]

        #df_media = self.pollutant_dataframe(df).mean()            
        #df_std_media = pd.DataFrame(df_media/self.limit*100)
        
        # Drop anno and ora columns
        df_media.drop(['anno','ora','limite', 'inquinante','data_ora'], inplace=True)
        #df_media.drop(['anno','ora','limite'], inplace=True)
        #df_std_media.drop(['anno','ora'], inplace=True)
        
        # Give to the remaining columns the name of the year
        df_media = pd.DataFrame(df_media)
        df_media.columns = [anno]
        #df_media = pd.DataFrame(df_media, columns=[anno])
        #df_std_media.columns = [anno]
        
        return df_media
        
        
    def _daily_avg(self, df, anno):
        """Returns the dailt average wrt the year of interest.
        
            df: dataframe to make computations on
            anno: year of interest
        """
        
        # Subselect the df of interest and sort by date
        df_inquinante = self.pollutant_dataframe(df)
        df_inquinante_sorted = df_inquinante.sort_values('data_ora')
        # Groupby date and take the average of the days
        df_groupby_date_avg = df_inquinante_sorted.groupby([pd.to_datetime(df['data_ora']).dt.date])\
                                                  .mean()
            
        # Divide the average by the limit
        #df_std_avg = df_groupby_date_avg/self.limit*100
        
        # Take the mean of the daily avg values
        df_daily_avg = df_inquinante_sorted.mean()
        #df_daily_avg = pd.DataFrame(df_std_avg.mean())
        
        # Drop anno and ora cols
        df_daily_avg.drop(['anno','ora', 'limite'], inplace=True)
        # Give to the remaining columns the name of the year
        df_daily_avg = pd.DataFrame(df_daily_avg, columns=[anno])
        
        return df_daily_avg
        
        
    def _yearly_avg(self, df, anno):
        """Returns the yearly average wrt the year of interest.
        
            df: dataframe to make computations on
            anno: year of interest
        """
        # Get the standardized average
        df_inquinante = self.pollutant_dataframe(df)
        df_avg_year = df_inquinante.groupby('anno').mean().T
        #df_std_avg = (df_avg_year/self.limit*100).T
        
        # Drop anno and ora cols
        df_avg_year.drop(['ora', 'limite'], inplace=True)
        #df_std_avg.drop(['ora'], inplace=True)
        
        # Give to the remaining columns the name of the year
        df_avg_year.columns = [anno]
        #df_std_avg.columns = [anno]
        
        return df_avg_year