import json
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from llama_index.core import SimpleDirectoryReader, PromptTemplate
from config import Settings 

class ItemSource(BaseModel):
    tool: str = Field(description="הכלי שייצר את התיעוד (למשל: cursor, claude_code, kiro)")
    file: str = Field(description="הנתיב המדויק של הקובץ שבו נמצא המידע")
    anchor: str = Field(description="כותרת הפסקה שבה נמצא המידע (למשל: #db או ## UI Rules)")

class Decision(BaseModel):
    id: str = Field(description="מזהה ייחודי, למשל: dec-001, dec-002")
    title: str = Field(description="כותרת ההחלטה")
    summary: str = Field(description="תקציר ההחלטה")
    tags: List[str] = Field(description="תגיות רלוונטיות")
    source: ItemSource
    observed_at: str = Field(description="תאריך ושעה בפורמט ISO, למשל: 2026-02-12T09:14:00+02:00")

class Rule(BaseModel):
    id: str = Field(description="מזהה ייחודי, למשל: rule-001")
    rule: str = Field(description="הכלל או ההנחיה")
    scope: str = Field(description="התחום שעליו הכלל חל (למשל: ui, api)")
    notes: str = Field(description="הערות נוספות")
    source: ItemSource
    observed_at: str = Field(description="תאריך ושעה בפורמט ISO")

class WarningItem(BaseModel):
    id: str = Field(description="מזהה ייחודי, למשל: warn-001")
    area: str = Field(description="האזור הרגיש")
    message: str = Field(description="תוכן האזהרה")
    severity: str = Field(description="רמת חומרה: low, medium, high")
    source: ItemSource
    observed_at: str = Field(description="תאריך ושעה בפורמט ISO")

class ExtractedItems(BaseModel):
    decisions: List[Decision]
    rules: List[Rule]
    warnings: List[WarningItem]


def extract_structured_data():
    print("📂 קורא את קבצי התיעוד (כולל תתי-תיקיות)...")
    
    data_path = "C:/Users/user1/Desktop/תכנותתת/שנה ב/AI/RAG/data-project"
    reader = SimpleDirectoryReader(
        input_dir=data_path, 
        recursive=True, 
        exclude_hidden=False,  
        required_exts=[".md"])
    documents = reader.load_data()
    
    if not documents:
        print("❌ לא נמצאו קבצי .md בתיקייה שציינת!")
        return

    full_text = ""
    file_list = []
    for doc in documents:
        file_path = doc.metadata.get('file_path', 'unknown')
        file_list.append({"path": file_path, "last_modified": datetime.now().isoformat()})
        full_text += f"\n\n--- FILE PATH: {file_path} ---\n{doc.text}\n"

    print("🧠 שולח ל-Cohere לחילוץ נתונים מובנים...")
    
    prompt = (
        "You are an expert technical architect analyzing project documentation.\n"
        "Extract technical decisions, coding rules, and critical warnings from the following text.\n"
        "Pay attention to the 'FILE PATH' markers to correctly fill the 'source.file' field for each item.\n"
        "Generate unique IDs for each item. For 'observed_at', use the current date.\n\n"
        f"Text to analyze:\n{full_text}\n\n"
        "CRITICAL INSTRUCTION: You MUST return ONLY valid, raw JSON. Do not add any text before or after.\n"
        "IMPORTANT: Keep 'summary', 'rule', and 'notes' fields VERY SHORT AND CONCISE (max 1-2 sentences) to save space!\n"
        "Use EXACTLY this structure:\n"
        "{\n"
        '  "decisions": [ {"id": "dec-1", "title": "...", "summary": "...", "tags": ["..."], "source": {"tool": "...", "file": "...", "anchor": "..."}, "observed_at": "..."} ],\n'
        '  "rules": [ {"id": "rule-1", "rule": "...", "scope": "...", "notes": "...", "source": {"tool": "...", "file": "...", "anchor": "..."}, "observed_at": "..."} ],\n'
        '  "warnings": [ {"id": "warn-1", "area": "...", "message": "...", "severity": "high", "source": {"tool": "...", "file": "...", "anchor": "..."}, "observed_at": "..."} ]\n'
        "}"
    )
    
    from llama_index.core.llms import ChatMessage
    
    messages = [ChatMessage(role="user", content=prompt)]
    chat_response = Settings.llm.chat(messages)
    
    response_text = str(chat_response).strip()
    
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    elif response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
        
    response_text = response_text.strip()
    
    if response_text.lower().startswith("assistant:"):
        response_text = response_text.split("assistant:", 1)[1].strip()
    

    if not response_text.endswith("}"):
        print("⚠️ אזהרה: ה-JSON נחתך באמצע! מנסה לתקן אוטומטית...")
        last_valid_comma = response_text.rfind("},{")
        if last_valid_comma != -1:
            response_text = response_text[:last_valid_comma + 1] + "\n  ]\n}"
        else:
            response_text = response_text + "\n}\n]\n}"

    try:
        extracted_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        print("❌ שגיאה: המודל עדיין לא החזיר JSON תקין. הנה מה שהוא ניסה להחזיר:")
        print(response_text)
        return
    
  
    final_json = {
        "schema_version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "sources": [
            {
                "tool": "multi-agent-extraction",
                "root_path": data_path,
                "files": file_list
            }
        ],
        "items": extracted_data
    }
    
    output_file = "structured_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_json, f, ensure_ascii=False, indent=2)
        
    print(f"✅ מדהים! הנתונים חולצו ונשמרו במבנה המושלם בקובץ: {output_file}")

if __name__ == "__main__":
    extract_structured_data()