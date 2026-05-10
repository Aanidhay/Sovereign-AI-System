# 🇮🇳 Personalized India Tour Guide

An interactive Streamlit application that provides personalized travel destination recommendations in India based on user preferences.

## Features

- **Personalized Recommendations**: Get travel suggestions based on your age group, interests, and preferred states
- **Comprehensive Dataset**: 100+ tourist destinations across India with detailed information
- **Smart Scoring System**: Intelligent algorithm that matches user preferences with destinations
- **Beautiful UI**: Modern, responsive interface with emojis and visual elements
- **Offline Functionality**: Works completely offline using CSV data

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this project
2. Navigate to the project directory:
   ```bash
   cd "TOUR GUIDE RECOMMENDER"
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit app:
```bash
streamlit run tour_guide_app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Enter Your Name**: Provide your name for personalized recommendations
2. **Select Age Group**: Choose your age range from the dropdown
3. **Choose Interests**: Select at least 2 interests from the available options
4. **Preferred States** (Optional): Select specific states you'd like to visit
5. **Get Recommendations**: Click the button to receive personalized suggestions

## Recommendation Algorithm

The system uses a weighted scoring algorithm:

- **Age Group Compatibility** (30%): Matches your age group with suitable destinations
- **Interest Overlap** (40%): Calculates overlap between your interests and destination activities
- **State Preference** (30%): Prioritizes destinations in your preferred states
- **Popularity Bonus**: Adds extra points based on destination popularity

## Dataset Structure

The `indian_tourist_places.csv` contains:

- **Place_Name**: Name of the destination
- **State**: Indian state/union territory
- **Suitable_Age_Group**: Recommended age range
- **Interests**: Available activities (comma-separated)
- **Place_Type**: Category of destination
- **Popularity_Score**: Rating from 1-10

## Sample Destinations

The dataset includes diverse destinations such as:

- **Beaches**: Baga Beach (Goa), Kovalam Beach (Kerala)
- **Historical**: Taj Mahal (Uttar Pradesh), Red Fort (Delhi)
- **Religious**: Varanasi Ghats (Uttar Pradesh), Meenakshi Temple (Tamil Nadu)
- **Adventure**: Rishikesh (Uttarakhand), Ladakh (Jammu & Kashmir)
- **Nature**: Munnar (Kerala), Shimla (Himachal Pradesh)

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS with gradients and cards

## Project Structure

```
TOUR GUIDE RECOMMENDER/
├── tour_guide_app.py          # Main Streamlit application
├── indian_tourist_places.csv  # Dataset of tourist destinations
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation
```

## Customization

### Adding New Destinations

To add new destinations, simply append rows to the `indian_tourist_places.csv` file following the existing format.

### Modifying Interests

Update the `interests_options` list in `tour_guide_app.py` to add or modify available interests.

### Adjusting Scoring Weights

Modify the weight percentages in the `calculate_recommendation_score()` function to change the recommendation algorithm.

## Troubleshooting

### Common Issues

1. **Dataset not found**: Ensure `indian_tourist_places.csv` is in the same directory as the app
2. **Port already in use**: Streamlit will automatically find an available port
3. **Dependencies not installed**: Run `pip install -r requirements.txt`

### Performance Tips

- The app works offline and requires minimal computational resources
- Dataset size can be expanded without performance issues
- Response time is typically under 1 second for recommendations

## Contributing

Feel free to contribute by:

- Adding more destinations to the dataset
- Improving the recommendation algorithm
- Enhancing the user interface
- Adding new features like weather integration or booking links

## License

This project is open source and available under the MIT License.

---

🌍 **Explore the incredible diversity of India with personalized recommendations!**
