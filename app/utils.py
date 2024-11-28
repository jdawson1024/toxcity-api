from typing import List, Dict, Tuple
import torch
from detoxify import Detoxify
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time

logger = logging.getLogger(__name__)

class ToxicityAnalyzer:
    def __init__(self, max_workers: int = 8):
        try:
            self.model = Detoxify('original', device='cpu')
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
            logger.info("ToxicityAnalyzer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ToxicityAnalyzer: {str(e)}")
            raise

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        """Process a batch of texts using Detoxify model"""
        try:
            with torch.no_grad():
                results = self.model.predict(texts)
            
            # Convert results to list of dictionaries
            batch_results = []
            for i in range(len(texts)):
                result = {}
                for key in results.keys():
                    # Convert tensor to float and handle NaN/Inf values
                    value = float(results[key][i])
                    result[key] = max(0.0, min(1.0, value))  # Clamp values between 0 and 1
                batch_results.append(result)
            
            return batch_results
            
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            raise

    async def process_texts(self, texts: List[str], batch_size: int) -> Tuple[List[Dict[str, float]], float]:
        """Process multiple texts in batches"""
        start_time = time.time()
        results = []
        
        try:
            # Process texts in batches
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_results = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.analyze_batch,
                    batch
                )
                results.extend(batch_results)

            processing_time = time.time() - start_time
            return results, processing_time
            
        except Exception as e:
            logger.error(f"Error in process_texts: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing texts: {str(e)}"
            )