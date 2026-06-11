export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        "deep-cosmos": "#0A0015",
        "temple-gold": "#FFB830",
        "saffron-fire": "#FF6B1A",
        "ruby-red": "#C0392B",
        "emerald-sacred": "#00BF72",
        "sapphire-deep": "#1A6BFF",
        "pearl-white": "#F5ECD7",
        "lotus-pink": "#FF4FA3",
        "cosmic-purple": "#7B2FBE"
      },
      fontFamily: {
        display: ["Cinzel Decorative", "serif"],
        cinzel: ["Cinzel", "serif"],
        body: ["Poppins", "sans-serif"],
        devanagari: ["Noto Serif Devanagari", "serif"]
      }
    }
  },
  plugins: []
};

