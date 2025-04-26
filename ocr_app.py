import streamlit as st
import tempfile
import os
from ocr.ocr_utils import process_receipt_with_groq
from ocr.database import init_db, insert_into_db, get_db_records

# Initialize the database at startup
init_db()

st.title("EcoStep OCR Analyzer")
st.write("Upload receipt images to analyze and store carbon footprint data.")

uploaded_files = st.file_uploader("Upload Receipts", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files):
        st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
        
        if st.button(f"Analyze {uploaded_file.name}", key=f"analyze_{i}"):
            with st.spinner("Analyzing receipt..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    temp_path = temp_file.name
                
                # Process the receipt
                receipt_items = process_receipt_with_groq(temp_path)
                
                # Remove temporary file
                os.unlink(temp_path)
                
                # Show results
                if receipt_items:
                    st.success(f"Receipt analyzed! Found {len(receipt_items)} items.")
                    
                    total_carbon_footprint = 0
                    
                    # Display each item in an expandable section
                    for i, item in enumerate(receipt_items):
                        with st.expander(f"Item {i+1}: {item.get('item_name', 'Unknown')}"):
                            st.write(f"**Item:** {item.get('item_name', 'N/A')}")
                            st.write(f"**Carbon Footprint:** {item.get('carbon_footprint', 0)} kg CO₂e")
                            st.write(f"**Quantity:** {item.get('quantity', 1)}")
                            st.write(f"**Category:** {item.get('category', 'Unknown')}")
                            
                            # Add to database
                            insert_into_db(item)
                            st.write("✅ Added to database")
                            
                            # Calculate total carbon footprint
                            carbon = item.get('carbon_footprint', 0)
                            quantity = item.get('quantity', 1)
                            total_carbon_footprint += carbon * quantity
                    
                    # Display total carbon footprint
                    st.metric("Total Carbon Footprint", f"{total_carbon_footprint:.2f} kg CO₂e")
                else:
                    st.error("Could not extract any items from the receipt.")

# Display database contents
if st.checkbox("Show Database Records"):
    results = get_db_records()
    
    if results:
        # Convert results to a list of dictionaries
        records = []
        for row in results:
            records.append({
                "ID": row[0],
                "Item": row[1],
                "Carbon Footprint (kg CO₂e)": row[2],
                "Quantity": row[3],
                "Category": row[4],
                "Date": row[5]
            })
        
        # Display as a dataframe
        st.dataframe(records)
    else:
        st.info("No records found in the database.")