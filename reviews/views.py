from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import Review
from .utils import classify_sentiment, tag_negative_review
from django.db.models import Count, Avg
from django.http import HttpResponse
import io
import csv
from datetime import datetime
from django.db.models.functions import TruncMonth

def upload_csv(request):
    message = ''
    saved_count = 0

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                message = 'Invalid file format. Please upload a CSV.'
            else:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                for row in reader:
                    review_id = row['review_id'].strip()
                    customer_name = row['customer_name'].strip()
                    review_text = row['review_text'].strip()
                    rating_str = row['rating'].strip()
                    date_str = row['date'].strip()

                    if Review.objects.filter(review_id=review_id).exists():
                        continue

                    try:
                        rating = int(rating_str)
                        if not (1 <= rating <= 5):
                            continue
                    except ValueError:
                        continue

                    try:
                        review_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        continue

                    sentiment = classify_sentiment(rating, review_text)
                    tags = tag_negative_review(review_text) if sentiment == 'negative' else ''

                    Review.objects.create(
                        review_id=review_id,
                        reviewer_name=customer_name,
                        review_text=review_text,
                        rating=rating,
                        review_date=review_date,
                        sentiment=sentiment,
                        tags=tags
                    )
                    saved_count += 1

                message = f'Upload complete. {saved_count} reviews saved.'
                return redirect('dashboard')
    else:
        form = CSVUploadForm()

    return render(request, 'reviews/upload.html', {'form': form, 'message': message})


def dashboard(request):
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']
    sentiments = Review.objects.values('sentiment').annotate(count=Count('id'))
    top_reviewers = Review.objects.values('reviewer_name').annotate(count=Count('id')).order_by('-count')[:5]
    return render(request, 'reviews/dashboard.html', {
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating or 0, 2),
        'sentiments': sentiments,
        'top_reviewers': top_reviewers,
    })


def monthly_report(request):
    monthly = (
        Review.objects
        .annotate(month=TruncMonth('review_date'))
        .values('month')
        .annotate(avg_rating=Avg('rating'), total=Count('id'))
        .order_by('month')
    )

    return render(request, 'reviews/monthly.html', {'monthly': monthly})

def export_reviews(request):
    if request.method == 'POST':
        try:
            min_rating = int(request.POST.get('min_rating', 1))
            max_rating = int(request.POST.get('max_rating', 5))
        except ValueError:
            min_rating, max_rating = 1, 5

        reviews = Review.objects.filter(rating__gte=min_rating, rating__lte=max_rating)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=filtered_reviews.csv'

        writer = csv.writer(response)
        writer.writerow(['review_id', 'reviewer_name', 'review_text', 'rating', 'review_date', 'sentiment', 'tags'])

        for r in reviews:
            writer.writerow([
                r.review_id, r.reviewer_name, r.review_text,
                r.rating, r.review_date, r.sentiment, r.tags
            ])
        return response

    return render(request, 'reviews/export.html')



def duplicate_reviews(request):
    duplicates = (
        Review.objects
        .values('review_text')
        .annotate(duplicate_count=Count('id'))
        .filter(duplicate_count__gt=1)
        .order_by('-duplicate_count')
    )

    return render(request, 'reviews/duplicates.html', {'duplicates': duplicates})