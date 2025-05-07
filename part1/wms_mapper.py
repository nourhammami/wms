import pandas as pd
from tkinter import filedialog, Tk, Button, Label, messagebox

class SKUMapper:
    def __init__(self, mapping_file):
        self.mapping_df = pd.read_excel(mapping_file)
        if 'SKU' not in self.mapping_df.columns or 'MSKU' not in self.mapping_df.columns:
            raise ValueError("Mapping file must contain 'SKU' and 'MSKU' columns")
        self.mapping_dict = dict(zip(self.mapping_df['SKU'], self.mapping_df['MSKU']))

    def map_sku(self, sku):
        if pd.isna(sku):
            return "UNKNOWN"
        # Handle combo products
        if '+' in sku:
            return '+'.join([self.mapping_dict.get(part.strip(), "UNKNOWN") for part in sku.split('+')])
        return self.mapping_dict.get(sku.strip(), "UNKNOWN")

    def process_file(self, sales_file):
        df = pd.read_excel(sales_file)
        if 'SKU' not in df.columns:
            raise ValueError("SKU column not found in sales data")
        df['MSKU'] = df['SKU'].apply(self.map_sku)
        df.to_excel("processed_sales.xlsx", index=False)
        return df

def open_gui():
    def run_mapper():
        try:
            mapping_file = filedialog.askopenfilename(title="Select WMS Mapping File")
            sales_file = filedialog.askopenfilename(title="Select Sales Data File")
            mapper = SKUMapper(mapping_file)
            mapper.process_file(sales_file)
            messagebox.showinfo("Success", "Sales data processed and saved as processed_sales.xlsx")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    window = Tk()
    window.title("SKU to MSKU Mapper")
    Label(window, text="Click the button to process your Sales Data").pack(pady=10)
    Button(window, text="Run Mapper", command=run_mapper).pack(pady=10)
    window.mainloop()

if __name__ == '__main__':
    open_gui()