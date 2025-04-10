def generate_analysis(team_name, stats):
    try:
        form_score = stats.get("form", 0)
        avg_goals = stats.get("avg_goals", 0)
        win_ratio = stats.get("win_ratio", 0)

        suggestion = "Bu matç üçün riskli görünür."
        if form_score >= 4 and win_ratio >= 60:
            suggestion = "Qələbə ehtimalı yüksəkdir."
        elif avg_goals >= 2.5:
            suggestion = "Qollar baxımından zəngin bir oyun gözlənilir."

        return f"AI Təhlil ({team_name}):\nForm: {form_score}/5\nQələbə Nisbəti: {win_ratio}%\nOrtalama Qol: {avg_goals}\n\nTövsiyə: {suggestion}"
    except Exception as e:
        return f"AI təhlilində xəta baş verdi: {str(e)}"
