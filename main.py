from app import app

app.config['SECRET_KEY'] = '1mht0m5830yKry2Y3w14kL8w05YF7T9C2Kb5O778Z0poWm3xkh7pb91JxO949Ks42n7LrE'
# Замените ключ перед запуском, для защиты от CSRF

if __name__ == '__main__':
    app.run(port=5057, debug=True)