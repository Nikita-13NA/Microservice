# recommendations/recommendations.pyfrom concurrent import futures
import random
from concurrent import futures
import grpc
from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub
from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="Мальтийский сокол"),
        BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
        BookRecommendation(id=3, title="Собака Баскервилей"),
        BookRecommendation(id=4, title="Автостопом по галактике"),
        BookRecommendation(id=5, title="Игра Эндера"),
        BookRecommendation(id=6, title="Гарри Поттер и философский камень"),
        BookRecommendation(id=7, title="457 градусов по фаренгейту"),
        BookRecommendation(id=8, title="Приключения Тома Сойера"),
        BookRecommendation(id=9, title="Разборки третьего уровня"),
        BookRecommendation(id=10, title="Перехватчик"),
        
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=1, title="Дюна"),
        BookRecommendation(id=2, title="Мечтают ли андроиды об электроовцах"),
        BookRecommendation(id=3, title="Игра Эндера"),
        BookRecommendation(id=4, title="Основание"),
        BookRecommendation(id=5, title="Бойня номер пять, или Крестовый поход детей"),
        BookRecommendation(id=6, title="Алмазный век, или Букварь для благородных девиц"),
        BookRecommendation(id=7, title="Песни Гипериона"),
        BookRecommendation(id=8, title="Чужак в стране чужой"),
        BookRecommendation(id=9, title="Князь Света"),
        BookRecommendation(id=10, title="Планета изгнания"),
        
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=7, title="Семь навыков высокоэффективных людей"),
        BookRecommendation(id=8, title="Как завоёвывать друзей и оказывать влияние на людей"),
        BookRecommendation(id=9, title="Человек в поисках смысла"),
        BookRecommendation(id=11, title="Атомные привычки"),
        BookRecommendation(id=12, title="Мой продуктивный год"),
        BookRecommendation(id=13, title="Измеряйте самое важное"),
        BookRecommendation(id=14, title="В работу с головой"),
        BookRecommendation(id=15, title="Книга о потерянном времени"),
        BookRecommendation(id=7, title="Код Таланта"),
        BookRecommendation(id=8, title="Зачем мы спим"),
       
    ],
}

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)
        return RecommendationResponse(recommendations=books_to_recommend)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50069")
    server.start()
    print("Server started. Listening on port 50079...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop(0)
        print("Server stopped.")

if __name__ == "__main__":
    serve()


