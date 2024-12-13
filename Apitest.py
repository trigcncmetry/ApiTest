import requests

# 定義 API 路徑
api_url = "https://api.practicesoftwaretesting.com/products"

def fetch_products_from_api(between=None, sort=None, page=1, per_page=10):
    # 構建查詢參數
    params = {
        'page': page,
        'per_page': per_page
    }

    # 如果有 'between' 參數，則添加到請求中
    if between:
        params['between'] = between
    
    # 如果有 'sort' 參數，則添加到請求中
    if sort:
        params['sort'] = sort

    # 發送 GET 請求
    response = requests.get(api_url, params=params)

    # 如果回應成功
    if response.status_code == 200:
        data = response.json()

        # 提取當前頁面資料
        products = data['data']

        # 如果頁面上有產品資料，顯示並返回
        if products:
            for product in products:
                print(f"Product ID: {product['id']}")
                print(f"Name: {product['name']}")
                print(f"Description: {product['description']}")
                print(f"Price: {product['price']}")
                print(f"Is Location Offer: {product['is_location_offer']}")
                print(f"Is Rental: {product['is_rental']}")
                print(f"Brand Name: {product['brand']['name']}")
                print(f"Category Name: {product['category']['name']}")
                print("-" * 40)
        
        # 回傳該頁面的資料和分頁資訊
        return data
    else:
        print(f"Error fetching data from API. Status code: {response.status_code}")
        return None

def fetch_all_products(between=None, sort=None):
    page = 1
    per_page = 10
    all_products = []

    # 初始請求獲取資料
    while True:
        print(f"Fetching page {page}...")
        data = fetch_products_from_api(between=between, sort=sort, page=page, per_page=per_page)

        if data is None:
            break

        all_products.extend(data['data'])

        # 如果當前頁是最後一頁，終止循環
        if data['current_page'] == data['last_page']:
            break
        
        # 移至下一頁
        page += 1

    print(f"Total products fetched: {len(all_products)}")
    return all_products

# 定義測試案例
def test_fetch_products():
    # 測試案例 1: 正確的篩選價格範圍 (10 到 15)
    print("Running test case 1: Price range between 10 and 15")
    fetch_all_products(between="price,10,15")

    # 測試案例 2: 按名稱升冪排序
    print("Running test case 2: Sort by name in ascending order")
    fetch_all_products(sort="name,asc")

    # 測試案例 3: 測試錯誤的參數，無效的價格範圍
    print("Running test case 3: Invalid price range")
    fetch_all_products(between="price,abc,xyz")

    # 測試案例 4: 測試分頁功能
    print("Running test case 4: Fetch multiple pages of products")
    fetch_all_products(between="price,5,20", sort="name,desc")

# 運行測試
test_fetch_products()
