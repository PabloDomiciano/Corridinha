import json
import os
from pathlib import Path

class ScoreManager:
    def __init__(self):
        # Cria o diretório data se não existir
        self.scores_file = Path("data/highscores.json")
        self.scores_file.parent.mkdir(exist_ok=True, parents=True)
        self.highscores = self.load_scores()
    
    def load_scores(self):
        """Carrega as pontuações do arquivo JSON"""
        try:
            if self.scores_file.exists():
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return []
    
    def save_scores(self):
        """Salva as pontuações no arquivo JSON"""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.highscores, f, indent=4)
            return True
        except IOError:
            return False
    
    def add_score(self, name, score):
        """Adiciona uma nova pontuação e mantém apenas as top 10"""
        self.highscores.append({"name": name, "score": score})
        
        # Ordena por pontuação (maior primeiro)
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        
        # Mantém apenas as 10 melhores
        self.highscores = self.highscores[:10]
        
        return self.save_scores()
    
    def is_highscore(self, score):
        """Verifica se uma pontuação é digna do placar"""
        if len(self.highscores) < 10:
            return True
        return score > self.highscores[-1]["score"]
    
    def get_highscores(self):
        """Retorna a lista de highscores"""
        return self.highscores