#!/usr/bin/env python3
"""
Policy Weekly Cache Manager

管理政策研究周报的搜索缓存，包括：
- 查看缓存统计
- 清理旧缓存
- 导出缓存数据
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

CACHE_BASE_PATH = Path(os.getenv("POLICY_CACHE_PATH", Path.home() / "policy-weekly" / "cache"))

def get_cache_stats() -> Dict:
    """获取缓存统计信息"""
    stats = {
        "total_files": 0,
        "total_size": 0,
        "topics": {}
    }

    for topic in ["ai-policy", "internet-policy", "finance-policy"]:
        topic_path = CACHE_BASE_PATH / topic
        if not topic_path.exists():
            continue

        files = list(topic_path.glob("*.json"))
        total_size = sum(f.stat().st_size for f in files)

        stats["topics"][topic] = {
            "files": len(files),
            "size": total_size,
            "size_mb": round(total_size / 1024 / 1024, 2),
            "weeks": [f.stem for f in files]
        }
        stats["total_files"] += len(files)
        stats["total_size"] += total_size

    stats["total_size_mb"] = round(stats["total_size"] / 1024 / 1024, 2)
    return stats

def clean_old_cache(weeks_to_keep: int = 4) -> int:
    """清理旧缓存，保留最近N周"""
    deleted_count = 0
    cutoff_date = datetime.now() - timedelta(weeks=weeks_to_keep)

    for topic in ["ai-policy", "internet-policy", "finance-policy"]:
        topic_path = CACHE_BASE_PATH / topic
        if not topic_path.exists():
            continue

        for cache_file in topic_path.glob("*.json"):
            # 从文件名解析日期 (格式: YYYY-Wnn)
            try:
                year_week = cache_file.stem
                year, week = year_week.split("-W")
                file_date = datetime.strptime(f"{year}-{week}-1", "%Y-%W-%w")

                if file_date < cutoff_date:
                    cache_file.unlink()
                    deleted_count += 1
                    print(f"Deleted: {cache_file.name}")
            except Exception as e:
                print(f"Error parsing {cache_file.name}: {e}")

    return deleted_count

def export_cache(output_path: str = None) -> None:
    """导出所有缓存数据到单个JSON文件"""
    if not output_path:
        output_path = f"policy-cache-export-{datetime.now().strftime('%Y%m%d')}.json"

    export_data = {}

    for topic in ["ai-policy", "internet-policy", "finance-policy"]:
        topic_path = CACHE_BASE_PATH / topic
        if not topic_path.exists():
            continue

        export_data[topic] = {}
        for cache_file in topic_path.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    export_data[topic][cache_file.stem] = json.load(f)
            except Exception as e:
                print(f"Error reading {cache_file}: {e}")

    with open(output_path, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"Exported {len(export_data)} topics to {output_path}")

def print_stats():
    """打印缓存统计"""
    stats = get_cache_stats()

    print("\n📊 Policy Weekly Cache Statistics\n")
    print("=" * 50)
    print(f"Total Files: {stats['total_files']}")
    print(f"Total Size: {stats['total_size_mb']} MB\n")

    for topic, data in stats["topics"].items():
        print(f"{topic}:")
        print(f"  Files: {data['files']}")
        print(f"  Size: {data['size_mb']} MB")
        print(f"  Weeks: {', '.join(data['weeks'])}")
        print()

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Manage Policy Weekly cache files"
    )
    parser.add_argument(
        "command",
        choices=["stats", "clean", "export"],
        help="Command to execute"
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=4,
        help="Weeks to keep when cleaning (default: 4)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path for export"
    )

    args = parser.parse_args()

    if args.command == "stats":
        print_stats()
    elif args.command == "clean":
        deleted = clean_old_cache(args.keep)
        print(f"\n✅ Deleted {deleted} old cache files")
        print_stats()
    elif args.command == "export":
        export_cache(args.output)

if __name__ == "__main__":
    main()
