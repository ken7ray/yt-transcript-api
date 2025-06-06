from flask import Flask, request, jsonify

# DEBUG: Check for missing dependency crash
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
except ImportError as e:
    print(f"❌ Import error: {e}")
    raise e

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Transcript API is running.'

@app.route('/api', methods=['GET'])
def get_transcript():
    print("📩 /api endpoint hit")
    video_id = request.args.get('id')
    print(f"🆔 Video ID received: {video_id}")

    if not video_id:
        print("⚠️ No video ID provided")
        return jsonify({'error': 'Missing video ID'}), 400

    try:
        print(f"🔍 Fetching transcript for: {video_id}")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([item['text'] for item in transcript_list])
        print("✅ Transcript fetched successfully")
        return jsonify({'video_id': video_id, 'transcript': full_text})
    except TranscriptsDisabled:
        print("❌ Transcripts are disabled for this video")
        return jsonify({'error': 'Transcripts are disabled for this video.'}), 403
    except NoTranscriptFound:
        print("❌ No transcript found for this video")
        return jsonify({'error': 'No transcript found for this video.'}), 404
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask app on port 8000")
    app.run(host='0.0.0.0', port=8000)
