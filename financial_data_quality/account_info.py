
    import pandas as pd

    class AccountInfo: 
      def init(self, account_metadata_file): 
        self.accounts = pd.read_csv(account_metadata_file)
      def get_account_info(self, account_name):
          return self.accounts[self.accounts['account_name'] == account_name]
